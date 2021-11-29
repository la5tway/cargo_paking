from datetime import datetime as dt
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageColor, ImageDraw, ImageFont

from .cargo import Cargo
from .container import Container
from .packer import Packer

DIR = Path.cwd()
OUTPUT_DIR = DIR / "image"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def render_img(
    container: Container,
    cargo_set: List[Cargo],
    save: bool = True,
    rotate: bool = False,
) -> Tuple[Packer, List[Cargo]]:
    fit_set, unfit_set = container.fitness_set(cargo_set)  # type: ignore
    packer = Packer(container, rotate)
    packer.add_cargo_set(fit_set)  # type: ignore

    fnt = ImageFont.truetype("arial.ttf", 100)

    image = Image.new(
        "RGB",
        (container.length + 50, container.width + 50),
        color=ImageColor.getrgb("white"),
    )

    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (container.point_bot_l, container.point_top_r),  # type: ignore
        outline=ImageColor.getrgb("black"),
    )

    for c in packer.cargo_set:
        draw.rectangle(
            (c.point_bot_l, c.point_top_r),  # type: ignore
            fill=ImageColor.getrgb("green"),
            outline=ImageColor.getrgb("red"),
        )
        draw.multiline_text(
            c.point_bot_l,  # type: ignore
            f"{c.name}\n{c.weight}",
            font=fnt,
            fill=ImageColor.getrgb("black"),
        )

    image.resize((1024, 720))

    if save:
        image.save(f"{OUTPUT_DIR}/{dt.now():%y%m%d_%H%M%S}.png", "PNG")

    image.show()

    return packer, unfit_set
