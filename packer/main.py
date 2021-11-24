from PIL import Image, ImageColor, ImageDraw, ImageFont

from cargo import Cargo
from kuzov import Kuzov
from scheduler import Scheduler

if __name__ == "__main__":
    kuzov = Kuzov(
        *(
            int(i)
            for i in input(
                "Введите характеристики кузова через пробел в порядке:\nдлина (мм), ширина (мм), высота (мм), грузоподъёмность (мм): "
            ).split()
        )
    )
    qty_cargo = int(input("Введите количество грузов в штуках: "))
    cargo_set = []
    for _ in range(qty_cargo):
        cargo = input(
            "Введите характеристики груза через пробел в порядке:\nдлина (мм), ширина (мм), высота (мм), вес (мм), наименование (не обязательно): "
        ).split()
        if len(cargo) > 4:
            cargo = Cargo(*[int(i) for i in cargo[:4]], cargo[4])
        else:
            cargo = Cargo(*[int(i) for i in cargo])
        cargo_set.append(cargo)
    unfit_cargo_set = []
    for cargo in cargo_set:
        if not kuzov.fitness(cargo):
            unfit_cargo_set.append(cargo)
            cargo_set.remove(cargo)
    scheduler = Scheduler(kuzov)
    scheduler.add_cargo_set(cargo_set)

    fnt = ImageFont.truetype("arial.ttf", 100)

    image = Image.new(
        "RGB", (kuzov.length + 50, kuzov.width + 50), color=ImageColor.getrgb("white")
    )
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (kuzov.point_bot_l, kuzov.point_top_r), outline=ImageColor.getrgb("black")
    )
    for c in scheduler.cargo_set:
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
    image.save("empty.png", "PNG")
    image.show()
    input("Нажмите Enter чтобы выйти ")
