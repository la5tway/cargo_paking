from operator import add, sub
from typing import Tuple


class Rectangle:
    op = add
    om = sub

    def __init__(
        self,
        length: int,
        width: int,
        height: int,
        weight: int,
        x: int = 0,
        y: int = 0,
        admittance: int = 25,
    ) -> None:
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.x = x
        self.y = y
        self.admittance = admittance

    def __repr__(self) -> str:
        attr = ", ".join((f"{a}={getattr(self, a)}" for a in self.__dict__))
        return f"{self.__class__.__name__}: {attr}"

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.length, self.width))

    @property
    def area(self) -> int:
        return self.length * self.width

    @property
    def area_with_admittance(self) -> int:
        return self.length_with_admittance * self.width_with_admittance

    @property
    def two_side_length(self) -> int:
        return self.length + self.width

    @property
    def two_side_length_with_admittance(self) -> int:
        return self.length_with_admittance + self.width_with_admittance

    @property
    def length_with_admittance(self) -> int:
        return self.om(self.length, self.admittance)

    @property
    def width_with_admittance(self) -> int:
        return self.om(self.width, self.admittance)

    @property
    def height_with_admittance(self) -> int:
        return self.om(self.height, self.admittance)

    @property
    def bottom(self) -> int:
        return self.y

    @property
    def bottom_with_admittance(self) -> int:
        return self.op(self.y, self.admittance)

    @property
    def top(self) -> int:
        return self.y + self.width

    @property
    def top_with_admittance(self) -> int:
        return self.om(self.top, self.admittance)

    @property
    def left(self) -> int:
        return self.x

    @property
    def left_with_admittance(self) -> int:
        return self.op(self.x, self.admittance)

    @property
    def right(self) -> int:
        return self.x + self.length

    @property
    def right_with_admittance(self) -> int:
        return self.om(self.right, self.admittance)

    @property
    def point_top_l(self) -> Tuple[int, ...]:
        return self.left, self.top

    @property
    def point_top_r(self) -> Tuple[int, ...]:
        return self.right, self.top

    @property
    def point_bot_r(self) -> Tuple[int, ...]:
        return self.right, self.bottom

    @property
    def point_bot_l(self) -> Tuple[int, ...]:
        return self.left, self.bottom

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def contains(self, rect: "Rectangle") -> bool:
        return (
            rect.y >= self.y
            and rect.x >= self.x
            and rect.top <= self.top
            and rect.right <= self.right
        )

    def contains_with_admittance(self, rect: "Rectangle") -> bool:
        return (
            rect.y >= self.y
            and rect.x >= self.x
            and rect.top_with_admittance <= self.top_with_admittance
            and rect.right_with_admittance <= self.right_with_admittance
        )

    def intersects(self, rect: "Rectangle") -> bool:
        return (self.bottom >= rect.top or self.top <= rect.bottom) and (
            self.left >= rect.right or self.right <= rect.left
        )

    def intersects_with_admittance(self, rect: "Rectangle", edges: bool = True) -> bool:
        if edges:
            result = (
                self.bottom_with_admittance < rect.bottom_with_admittance
                or self.top_with_admittance > rect.top_with_admittance
                or self.left_with_admittance < rect.left_with_admittance
                or self.right_with_admittance > rect.right_with_admittance
            )
        else:
            result = (
                self.bottom_with_admittance <= rect.bottom_with_admittance
                or self.top_with_admittance >= rect.top_with_admittance
                or self.left_with_admittance <= rect.left_with_admittance
                or self.right_with_admittance >= rect.right_with_admittance
            )
        return result

    def fitness(self, rect: "Rectangle") -> bool:
        if (
            self.two_side_length_with_admittance > rect.two_side_length_with_admittance
            and self.weight > rect.weight
        ):
            return True
