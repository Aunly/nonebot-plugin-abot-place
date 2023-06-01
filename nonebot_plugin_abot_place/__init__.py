import re
from typing import Union

from nonebot.adapters.onebot.v11 import Bot as V11_Bot
from nonebot.adapters.onebot.v12 import Bot as V12_Bot
from nonebot.params import Depends, ShellCommandArgs
from nonebot.plugin import on_command, on_shell_command
from nonebot.rule import ArgumentParser, Namespace
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata

from .config import plugin_config,__version__
from .database import DB
from .draw import color_plant_img, draw_pixel, get_draw_line, zoom_merge_chunk
from .utils import get_image, get_reply, get_sender


__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-abot-place",
    description="移植于 ABot 的画板插件，可以和所有的 bot 用户一起画画！",
    usage="指令：查看画板、查看色板、画板作画\n详细说明请查看项目主页",
    homepage="https://github.com/Aunly/nonebot-plugin-abot-place",
    supported_adapters={"~onebot.v11", "~onebot.v12"},
    extra={
        "author": "djkcyl & Well404",
        "version": __version__,
        "priority": 1,
    },
)

parser = ArgumentParser()
parser.add_argument("numbers", type=int, nargs="*")


place_view = on_shell_command("查看画板", aliases=plugin_config.place_view_aliases, parser=parser, block=False)
color_view = on_command("查看色板", aliases=plugin_config.color_view_aliases, block=False)
place_draw = on_shell_command("画板作画", aliases=plugin_config.place_draw_aliases, parser=parser, block=False)


@place_view.handle()
async def view_image_handle(
    bot: Union[V11_Bot, V12_Bot], chunk: Namespace = ShellCommandArgs(), reply=Depends(get_reply, use_cache=False)
):
    if chunk and len(chunk.numbers) == 2:
        data = get_draw_line(*chunk.numbers)
    else:
        data = zoom_merge_chunk()
    await place_view.finish(reply + await get_image(data, bot))


@color_view.handle()
async def view_color_handle(bot: Union[V11_Bot, V12_Bot], reply=Depends(get_reply, use_cache=False)):
    await color_view.finish(reply + await get_image(color_plant_img, bot))


@place_draw.handle()
async def place_draw_prehandle(
    bot: Union[V11_Bot, V12_Bot],
    state: T_State,
    reply=Depends(get_reply, use_cache=False),
    coordinates: Namespace = ShellCommandArgs(),
):
    try:
        coordinates = [x for x in coordinates.numbers]
        if len(coordinates) > 5:
            raise ValueError
    except Exception:
        await place_draw.send(reply + "你输入的数值错误\n请重新输入想要作画的区块坐标" + await get_image(get_draw_line(), bot))
    if len(coordinates) < 2:
        await place_draw.send(reply + "请发送想要作画的区块坐标：" + await get_image(get_draw_line(), bot))
    elif len(coordinates) < 4:
        state["chunk"] = f"{coordinates[0]} {coordinates[1]}"
    elif len(coordinates) < 5:
        state["chunk"] = f"{coordinates[0]} {coordinates[1]}"
        state["pixel"] = f"{coordinates[2]} {coordinates[3]}"
    else:
        state["chunk"] = f"{coordinates[0]} {coordinates[1]}"
        state["pixel"] = f"{coordinates[2]} {coordinates[3]}"
        state["color_raw"] = coordinates[4]


@place_draw.got("chunk")
async def place_draw_getchunk(bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False)):
    arg = str(state["chunk"])
    if arg == "取消":
        await place_draw.finish()

    p = re.compile(r"^(\d{1,2})[|;:,，\s](\d{1,2})$")
    if not p.match(arg):
        await place_draw.reject(reply + "请输入正确的坐标，格式：x,y")

    x, y = p.match(arg).groups()
    if 31 >= int(x) >= 0 and 31 >= int(y) >= 0:
        if not state.get("pixel"):
            await place_draw.send(reply + "请输入想要绘制的像素坐标：\n" + await get_image(get_draw_line(int(x), int(y)), bot))
        state["chunk_x"], state["chunk_y"] = int(x), int(y)
    else:
        await place_draw.reject(reply + "坐标超出范围（0-31），请重新输入")


@place_draw.got("pixel")
async def place_draw_getpixel(bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False)):
    arg = str(state["pixel"])
    if arg == "取消":
        await place_draw.finish()

    p = re.compile(r"^(\d{1,2})[|;:,，\s](\d{1,2})$")
    if not p.match(arg):
        await place_draw.reject(reply + "请输入正确的坐标，格式：x,y")

    x, y = p.match(arg).groups()
    if 31 >= int(x) >= 0 and 31 >= int(y) >= 0:
        if not state.get("color_raw"):
            await place_draw.send(reply + "请输入想要绘制的颜色：\n" + await get_image(color_plant_img, bot))
        state["pixel_x"], state["pixel_y"] = int(x), int(y)
    else:
        await place_draw.reject(reply + "坐标超出范围（0-31），请重新输入")


@place_draw.got("color_raw")
async def place_draw_getcolor(
    bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False)
):  # sourcery skip: use-fstring-for-concatenation
    arg = str(state["color_raw"])
    if arg == "取消":
        await place_draw.finish()

    p = re.compile(r"^(\d{1,3})$")
    if not p.match(arg):
        await place_draw.reject(reply + "颜色超出范围（0-255），请重新输入")

    color = int(arg)
    if 256 >= color >= 1:
        state["color"] = color
    else:
        await place_draw.reject(reply + "坐标超出范围（0-31），请重新输入")


@place_draw.handle()
async def place_draw_handle(
    bot: Union[V11_Bot, V12_Bot],
    state: T_State,
    sender=Depends(get_sender, use_cache=False),
    reply=Depends(get_reply, use_cache=False),
):
    member, group = sender

    fill_id = await DB.async_fill_pixel(
        member, group, state["color"], state["chunk_x"], state["chunk_y"], state["pixel_x"], state["pixel_y"]
    )
    draw_pixel(state["chunk_x"], state["chunk_y"], state["pixel_x"], state["pixel_y"], state["color"])
    await place_draw.finish(
        reply + f"ID: {fill_id} 绘制成功\n" + await get_image(get_draw_line(state["chunk_x"], state["chunk_y"]), bot)
    )
