from datetime import datetime as dt

from PIL import Image, ImageColor, ImageDraw, ImageFont

from packer.cargo import Cargo
from packer.container import Container
from packer.packer import Packer


def render_img(
    container: Container,
    cargo_set: list[Cargo],
    save: bool = True,
    rotate: bool = False,
):
    fit_set, unfit_set = container.fitness_set(cargo_set)
    packer = Packer(container, rotate)
    packer.add_cargo_set(fit_set)

    fnt = ImageFont.truetype("arial.ttf", 100)

    image = Image.new(
        "RGB",
        (container.length + 50, container.width + 50),
        color=ImageColor.getrgb("white"),
    )
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (container.point_bot_l, container.point_top_r),
        outline=ImageColor.getrgb("black"),
    )
    for c in packer.cargo_set:
        draw.rectangle(
            (c.point_bot_l, c.point_top_r),
            fill=ImageColor.getrgb("green"),
            outline=ImageColor.getrgb("red"),
        )
        draw.multiline_text(
            c.point_bot_l,
            f"{c.name}\n{c.weight}",
            font=fnt,
            fill=ImageColor.getrgb("black"),
        )
    image.resize((1024, 720))
    if save:
        image.save(f"{dt.now():%y%m%d_%H%M%S}.png", "PNG")
    unfit_set += packer.unfit_cargo_set
    if len(unfit_set) > 0:
        print("Не уместившийся груз:")
        for c in unfit_set:
            print(f"- {c.name}")
    image.show()

