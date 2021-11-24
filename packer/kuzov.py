from rectangle import Rectangle


class Kuzov(Rectangle):
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
        super().__init__(
            length,
            width,
            height,
            weight,
            x=x,
            y=y,
            admittance=admittance
        )
        self.weight_left = self.weight
