from typing import Union

from nonebot.adapters.onebot.v11 import Bot as V11_Bot
from nonebot.adapters.onebot.v12 import Bot as V12_Bot
from nonebot.params import Depends, ShellCommandArgs
from nonebot.plugin import on_command, on_shell_command
from nonebot.rule import ArgumentParser, Namespace

from .database import DB
from .draw import color_plant_img, draw_pixel, get_draw_line, zoom_merge_chunk
from .utils import get_image, get_reply, get_sender

parser = ArgumentParser()
parser.add_argument("numbers", type=int, nargs="*")


view_image = on_shell_command("查看画板", parser=parser, block=False)
view_color = on_command("查看色板", block=False)
fast_place = on_shell_command("快捷作画", parser=parser, block=False)


@view_image.handle()
async def view_image_handle(
    bot: Union[V11_Bot, V12_Bot], chunk: Namespace = ShellCommandArgs(), reply=Depends(get_reply)
):
    if chunk and len(chunk.numbers) == 2:
        data = get_draw_line(*chunk.numbers)
    else:
        data = zoom_merge_chunk()
    await view_image.finish(reply + await get_image(data, bot))


@view_color.handle()
async def view_color_handle(bot: Union[V11_Bot, V12_Bot], reply=Depends(get_reply)):
    await view_color.finish(reply + await get_image(color_plant_img, bot))


@fast_place.handle()
async def fast_place_handle(
    bot: Union[V11_Bot, V12_Bot],
    sender=Depends(get_sender),
    reply=Depends(get_reply),
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


# @channel.use(
#    ListenerSchema(
#        listening_events=[GroupMessage],
#        inline_dispatchers=[
#            Twilight(
#                [FullMatch("画板作画")],
#            )
#        ],
#        decorators=[
#            Function.require("ABotPlace"),
#            Permission.require(),
#            Interval.require(30),
#        ],
#    )
# )
# async def place_draw(group: Group, member: Member):
#    @Waiter.create_using_function(listening_events=[GroupMessage], using_decorators=[Permission.require()])
#    async def waiter_chunk(waiter1_group: Group, waiter1_member: Member, waiter1_message: MessageChain):
#        if waiter1_group.id != group.id or waiter1_member.id != member.id:
#            return
#        if waiter1_message.asDisplay() == "取消":
#            return False
#        p = re.compile(r"^(\d{1,2})[|;:,，\s](\d{1,2})$")
#        if p.match(waiter1_message.asDisplay()):
#            x, y = p.match(waiter1_message.asDisplay()).groups()
#            if 31 >= int(x) >= 0 and 31 >= int(y) >= 0:
#                return int(x), int(y)
#            else:
#                await safeSendGroupMessage(
#                    waiter1_group,
#                    MessageChain.create(
#                        At(waiter1_member),
#                        Plain("坐标超出范围（0-31），请重新输入"),
#                    ),
#                )
#        else:
#            await safeSendGroupMessage(
#                waiter1_group,
#                MessageChain.create(
#                    At(waiter1_member),
#                    Plain("请输入正确的坐标，格式：x,y"),
#                ),
#            )
#
#    @Waiter.create_using_function(listening_events=[GroupMessage], using_decorators=[Permission.require()])
#    async def waiter_color(waiter1_group: Group, waiter1_member: Member, waiter1_message: MessageChain):
#        if waiter1_group.id == group.id and waiter1_member.id == member.id:
#            if waiter1_message.asDisplay() == "取消":
#                return False
#            p = re.compile(r"^(\d{1,3})$")
#            if p.match(waiter1_message.asDisplay()):
#                color = int(waiter1_message.asDisplay())
#                if 256 >= color >= 1:
#                    return color
#                else:
#                    await safeSendGroupMessage(
#                        waiter1_group,
#                        MessageChain.create(
#                            At(waiter1_member),
#                            Plain(" 颜色超出范围（0-255），请重新输入"),
#                        ),
#                    )
#
#    await safeSendGroupMessage(
#        group,
#        MessageChain.create(At(member), Plain(" 请发送想要作画的区块坐标：\n"), Image(data_bytes=get_draw_line())),
#    )
#
#    try:
#        chunk = await asyncio.wait_for(inc.wait(waiter_chunk), 60)
#        if chunk:
#            chunk_x, chunk_y = chunk
#            await safeSendGroupMessage(
#                group,
#                MessageChain.create(
#                    At(member),
#                    Plain(" 请输入想要绘制的像素坐标：\n"),
#                    Image(data_bytes=get_draw_line(chunk_x, chunk_y)),
#                ),
#            )
#            pixel = await asyncio.wait_for(inc.wait(waiter_chunk), 60)
#            if pixel:
#                pixel_x, pixel_y = pixel
#                await safeSendGroupMessage(
#                    group,
#                    MessageChain.create(
#                        At(member),
#                        Plain(" 请输入想要绘制的颜色：\n"),
#                        Image(data_bytes=color_plant_img),
#                    ),
#                )
#                color = await asyncio.wait_for(inc.wait(waiter_color), 60)
#                if color:
#                    fill_id = await DB.async_fill_pixel(member, group, color, chunk_x, chunk_y, pixel_x, pixel_y)
#                    draw_pixel(chunk_x, chunk_y, pixel_x, pixel_y, color)
#                    await safeSendGroupMessage(
#                        group,
#                        MessageChain.create(
#                            f"ID: {fill_id} 绘制成功\n",
#                            Image(data_bytes=get_draw_line(chunk_x, chunk_y)),
#                        ),
#                    )
#            else:
#                await safeSendGroupMessage(group, MessageChain.create(At(member), Plain(" 操作已取消")))
#                return
#
#        else:
#            await safeSendGroupMessage(group, MessageChain.create(At(member), Plain(" 操作已取消")))
#            return
#
#    except asyncio.TimeoutError:
#        await safeSendGroupMessage(
#            group,
#            MessageChain.create(At(member), Plain(" 等待超时，操作已取消")),
#        )
#        return


# 快捷绘制
