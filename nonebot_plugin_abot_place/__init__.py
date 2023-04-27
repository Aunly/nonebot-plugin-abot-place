import re
from typing import Union

from nonebot.adapters.onebot.v11 import Bot as V11_Bot
from nonebot.adapters.onebot.v12 import Bot as V12_Bot
from nonebot.params import ArgPlainText, Depends, ShellCommandArgs
from nonebot.plugin import on_command, on_shell_command
from nonebot.rule import ArgumentParser, Namespace
from nonebot.typing import T_State

from .database import DB
from .draw import color_plant_img, draw_pixel, get_draw_line, zoom_merge_chunk
from .utils import get_image, get_reply, get_sender

parser = ArgumentParser()
parser.add_argument("numbers", type=int, nargs="*")


view_image = on_shell_command("查看画板", parser=parser, block=False)
view_color = on_command("查看色板", block=False)
fast_place = on_shell_command("快捷作画", parser=parser, block=False)
place_draw = on_command("画板作画", block=False)


@view_image.handle()
async def view_image_handle(
    bot: Union[V11_Bot, V12_Bot], chunk: Namespace = ShellCommandArgs(), reply=Depends(get_reply, use_cache=False)
):
    if chunk and len(chunk.numbers) == 2:
        data = get_draw_line(*chunk.numbers)
    else:
        data = zoom_merge_chunk()
    await view_image.finish(reply + await get_image(data, bot))


@view_color.handle()
async def view_color_handle(bot: Union[V11_Bot, V12_Bot], reply=Depends(get_reply, use_cache=False)):
    await view_color.finish(reply + await get_image(color_plant_img, bot))


@fast_place.handle()
async def fast_place_handle(
    bot: Union[V11_Bot, V12_Bot],
    sender=Depends(get_sender, use_cache=False),
    reply=Depends(get_reply, use_cache=False),
    coordinates: Namespace = ShellCommandArgs(),
):  # sourcery skip: use-fstring-for-concatenation
    try:
        chunk_x, chunk_y, pixel_x, pixel_y, color = [int(x) for x in coordinates.numbers]
    except Exception:
        await fast_place.finish(reply + "你输入的数值错误，无法绘制，请检查后重发")

    member, group = sender  # type: ignore
    if 31 >= chunk_x >= 0 and 31 >= chunk_y >= 0 and 31 >= pixel_x >= 0 and 31 >= pixel_y >= 0 and 256 >= color >= 1:
        fill_id = await DB.async_fill_pixel(member, group, color, chunk_x, chunk_y, pixel_x, pixel_y)
        draw_pixel(chunk_x, chunk_y, pixel_x, pixel_y, color)
        img = await get_image(get_draw_line(chunk_x, chunk_y), bot)
        await fast_place.finish(reply + f"ID: {fill_id} 绘制成功\n" + img)
    else:
        await fast_place.finish(reply + "你输入的数值错误，无法绘制，请检查后重发")


@place_draw.handle()
async def place_draw_prehandle(bot: Union[V11_Bot, V12_Bot], reply=Depends(get_reply, use_cache=False)):
    # sourcery skip: use-fstring-for-concatenation
    await place_draw.send(reply + "请发送想要作画的区块坐标：" + await get_image(get_draw_line(), bot))


@place_draw.got("chunk")
async def place_draw_getchunk(
    bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False), arg=ArgPlainText("chunk")
):
    if arg == "取消":
        await place_draw.finish()

    p = re.compile(r"^(\d{1,2})[|;:,，\s](\d{1,2})$")
    if not p.match(arg):
        await place_draw.reject(reply + "请输入正确的坐标，格式：x,y")

    x, y = p.match(arg).groups()
    if 31 >= int(x) >= 0 and 31 >= int(y) >= 0:
        await place_draw.send(reply + "请输入想要绘制的像素坐标：\n" + await get_image(get_draw_line(int(x), int(y)), bot))
        state["chunk_x"], state["chunk_y"] = int(x), int(y)
    else:
        await place_draw.reject(reply + "坐标超出范围（0-31），请重新输入")


@place_draw.got("pixel")
async def place_draw_getpixel(
    bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False), arg=ArgPlainText("pixel")
):
    if arg == "取消":
        await place_draw.finish()

    p = re.compile(r"^(\d{1,2})[|;:,，\s](\d{1,2})$")
    if not p.match(arg):
        await place_draw.reject(reply + "请输入正确的坐标，格式：x,y")

    x, y = p.match(arg).groups()
    if 31 >= int(x) >= 0 and 31 >= int(y) >= 0:
        await place_draw.send(reply + "请输入想要绘制的颜色：\n" + await get_image(color_plant_img, bot))
        state["pixel_x"], state["pixel_y"] = int(x), int(y)
    else:
        await place_draw.reject(reply + "坐标超出范围（0-31），请重新输入")


@place_draw.got("color")
async def place_draw_getcolor(
    bot: Union[V11_Bot, V12_Bot], state: T_State, reply=Depends(get_reply, use_cache=False), arg=ArgPlainText("color")
):  # sourcery skip: use-fstring-for-concatenation
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
