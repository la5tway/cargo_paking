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
    packer, unfit_set = render_img(container, cargo_set, rotate=True)
    print(f"Всего упаковано грузов: {len(packer.cargo_set)} шт.")
    print(f"Вес упакованных грузов: {packer.used_weight()} кг")
    print(f"Занятая площадь: {packer.used_area_m2()} м2")
    unfit_set += packer.unfit_cargo_set
    if len(unfit_set) > 0:
        print("Не уместившийся груз:")
        for cargo in unfit_set:
            print(f"- {cargo.name} ({cargo})")
    input("Нажмите Enter чтобы выйти ")