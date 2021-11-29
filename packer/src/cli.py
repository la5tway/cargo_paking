from .cargo import Cargo
from .container import Container
from .render_img import render_img


def cli() -> None:
    container = Container(
        *(
            int(i)
            for i in input(
                "Введите характеристики кузова через пробел в порядке:\nдлина (мм), ширина (мм), высота (мм), грузоподъёмность (кг): "
            ).split()
        )
    )
    qty_cargo = int(input("Введите количество груза в штуках: "))
    cargo_set = []
    for _ in range(qty_cargo):
        cargo = input(
            "Введите характеристики груза через пробел в порядке:\nдлина (мм), ширина (мм), высота (мм), вес (кг), наименование (не обязательно): "
        ).split()
        if len(cargo) > 4:
            cargo = Cargo(*[int(i) for i in cargo[:4]], cargo[4])
        else:
            cargo = Cargo(*[int(i) for i in cargo])
        cargo_set.append(cargo)
    render_img(container, cargo_set, rotate=True)
    input("Нажмите Enter чтобы выйти ")