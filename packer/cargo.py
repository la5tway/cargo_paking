from rectangle import Rectangle
from itertools import count
from operator import add, sub


def _cargo_name_generator():
    _count = count()
    next(_count)
    while True:
        number = next(_count)
        yield f"Cargo {number}"


cargo_name_generator = _cargo_name_generator()


class Cargo(Rectangle):
    op = sub
    om = add

    def __init__(
        self,
        length: int,
        width: int,
        height: int,
        weight: int,
        name: str = None,
        x: int = 0,
        y: int = 0,
        admittance: int = 25,
    ) -> None:
        super().__init__(length, width, height, weight, x=x, y=y, admittance=admittance)
        if name is None:
            self.name = next(cargo_name_generator)

    @property
    def weight_per_area(self) -> float:
        return self.weight / self.area_with_admittance

    def rotate(self) -> None:
        self.x, self.y = self.y, self.x

    def intersects_with_admittance(self, rect: "Rectangle", edges: bool = True) -> bool:
        if edges:
            result = (
                self.bottom_with_admittance > rect.top_with_admittance
                or self.top_with_admittance < rect.bottom_with_admittance
            ) and (
                self.left_with_admittance > rect.right_with_admittance
                or self.right_with_admittance < rect.left_with_admittance
            )
        else:
            result = (
                self.bottom_with_admittance >= rect.top_with_admittance
                or self.top_with_admittance <= rect.bottom_with_admittance
            ) and (
                self.left_with_admittance >= rect.right_with_admittance
                or self.right_with_admittance <= rect.left_with_admittance
            )
        return result
