from io import BytesIO
from pathlib import Path
from loguru import logger

from PIL import Image, ImageDraw, ImageFont

from .color import color_plant_source
from .database import data_dir

image_path = data_dir.joinpath("image")
image_path.mkdir(exist_ok=True,parents=True)
font_path = Path(__file__).parent.joinpath("static", "sarasa-mono-sc-semibold.ttf")
font = ImageFont.truetype(str(font_path.absolute()), 20)


if image_path.joinpath("full.png").exists():
    full_image = Image.open(image_path.joinpath("full.png"))
else:
    full_image = Image.new("RGB", (1024, 1024), (255, 255, 255))
    full_image.save(image_path.joinpath("full.png"))

if image_path.joinpath("color_plant.png").exists():
    color_plant_img = image_path.joinpath("color_plant.png").read_bytes()
else:
    logger.info("正在绘制色盘")
    color_plant_img = Image.new("RGB", (1866, 1000), (255, 255, 255))
    line = 0
    draw = ImageDraw.Draw(color_plant_img)

    i = 0
    for x, colors in enumerate(color_plant_source):
        for y, color in enumerate(colors):
            draw.ellipse(
                (
                    20 + x * 20 + x * 24,
                    48 + y * 20 + y * 88,
                    20 + x * 20 + 64 + x * 24,
                    48 + y * 20 + 64 + y * 88,
                ),
                fill=color,
                outline="black",
                width=2,
            )
            i += 1

            if i < 10:
                it = f"00{i}"
            elif i < 100:
                it = f"0{i}"
            else:
                it = f"{i}"

            draw.text(
                (36 + x * 20 + x * 24, 18 + y * 20 + y * 88),
                it,
                fill="black",
                font=font,
            )

    color_plant_img.save(image_path.joinpath("color_plant.png"))
    color_plant_bio = BytesIO()
    color_plant_img.save(color_plant_bio, "png")
    color_plant_img = color_plant_bio.getvalue()

color_plant = []
for color in color_plant_source:
    color_plant += color

place_chunk = {}

logger.info("正在加载画板区块")
for chunk_x in [str(x) for x in range(32)]:
    for chunk_y in [str(x) for x in range(32)]:
        if image_path.joinpath(f"{chunk_x}_{chunk_y}.png").exists():
            img = Image.open(BytesIO(image_path.joinpath(f"{chunk_x}_{chunk_y}.png").read_bytes()))
            if chunk_x in place_chunk:
                place_chunk[chunk_x][chunk_y] = img
            else:
                place_chunk[chunk_x] = {chunk_y: img}
        else:
            img = Image.new("RGB", (32, 32), (255, 255, 255))
            if chunk_x in place_chunk:
                place_chunk[chunk_x][chunk_y] = img
            else:
                place_chunk[chunk_x] = {chunk_y: img}
            img.save(image_path.joinpath(f"{chunk_x}_{chunk_y}.png"))
logger.info("画板区块加载完成")


def merge_chunk():
    global full_image
    logger.info("正在合并区块全图")
    for chunk_x in [str(x) for x in range(32)]:
        for chunk_y in [str(x) for x in range(32)]:
            full_image.paste(place_chunk[chunk_x][chunk_y], (int(chunk_x) * 32, int(chunk_y) * 32))

    full_image.save(image_path.joinpath("full.png"))
    full_bio = BytesIO()
    full_image.save(full_bio, "png")
    return full_bio.getvalue()


def zoom_merge_chunk(zoom: int = 3):
    global full_image
    zoom_image = full_image.resize((full_image.width * zoom, full_image.height * zoom), Image.NEAREST)
    zoom_bio = BytesIO()
    zoom_image.save(zoom_bio, "png")
    return zoom_bio.getvalue()


def get_draw_line(chunk_x: int = None, chunk_y: int = None):  # type: ignore
    if chunk_x is not None and chunk_y is not None:
        need_draw = place_chunk[str(chunk_x)][str(chunk_y)].resize((1024, 1024), Image.NEAREST)
        title = f"区块：{chunk_x}_{chunk_y}"
    else:
        need_draw = full_image
        title = "全图"

    logger.info(f"正在绘制棋盘：{title}")
    draw = ImageDraw.Draw(need_draw)
    y_line = False
    img = Image.new("RGB", (1224, 1224), (255, 255, 255))
    for chunk_x in [str(x) for x in range(32)]:  # type: ignore
        for chunk_y in [str(x) for x in range(32)]:  # type: ignore
            if not y_line:
                draw.line((int(chunk_y) * 32, 0, int(chunk_y) * 32, 1024), fill="black", width=1)
        y_line = True
        draw.line((0, int(chunk_x) * 32, 1024, int(chunk_x) * 32), fill="black", width=1)

    img.paste(need_draw, (100, 100))
    draw = ImageDraw.Draw(img)
    draw.line((1124, 100, 1124, 1124), fill="black", width=1)
    draw.line((100, 1124, 1124, 1124), fill="black", width=1)

    for i in range(32):
        t = f"0{i}" if i < 10 else str(i)
        draw.text((74, 106 + i * 32), t, fill="black", font=font)
        draw.text((1130, 106 + i * 32), t, fill="black", font=font)

        draw.text((107 + i * 32, 74), t, fill="black", font=font)
        draw.text((107 + i * 32, 1130), t, fill="black", font=font)

    draw.text((10, 10), title, fill="black", font=font)

    bio = BytesIO()
    img.save(bio, "png")
    return bio.getvalue()


def draw_pixel(chunk_x: int, chunk_y: int, pixel_x: int, pixel_y: int, color: int):
    img = place_chunk[str(chunk_x)][str(chunk_y)]
    draw = ImageDraw.Draw(img)
    draw.point((pixel_x, pixel_y), fill=color_plant[color - 1])
    img.save(image_path.joinpath(f"{chunk_x}_{chunk_y}.png"))
    merge_chunk()
