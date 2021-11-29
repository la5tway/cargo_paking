import itertools
from copy import deepcopy
from itertools import chain
from typing import List, Optional, Tuple, Union

from .cargo import Cargo
from .container import Container


class Packer:
    def __init__(
        self,
        container: Container,
        rotate: bool = False,
    ) -> None:
        self.container = deepcopy(container)
        self.rotate = rotate
        self.cargo_set: List[Cargo] = []
        self.unfit_cargo_set: List[Cargo] = []
        self._max_container_set = [deepcopy(container)]

    def used_area(self) -> float:
        return sum(cargo.area_with_admittance for cargo in self.cargo_set)

    def validate_packing(self):
        container = deepcopy(self.container)
        len_cargo_set = len(self.cargo_set)
        if len_cargo_set <= 1:
            return

        for cargo in self.cargo_set:
            if not container.contains(cargo):
                raise Exception("Cargo placed outside container")

        for c1 in range(0, len_cargo_set - 2):
            for c2 in range(c1 + 1, len_cargo_set - 1):
                if self.cargo_set[c1].intersects_with_admittance(self.cargo_set[c2]):
                    raise Exception("Cargo collision detected")

    def _cargo_fitness(self, max_container: Container, cargo: Cargo) -> Optional[int]:
        if max_container._two_side_fitness(cargo):
            if cargo.weight <= self.container.weight_left:
                return max_container.left
        return None

    def _select_position(
        self, cargo: Cargo
    ) -> Union[Tuple[Cargo, Container], Tuple[None, None]]:
        if not self._max_container_set:
            return None, None

        fitn = (
            (cf, max_container, cargo)
            for max_container in self._max_container_set
            if (cf := self._cargo_fitness(max_container, cargo)) is not None
        )
        fitr = []
        if self.rotate:
            ccargo = deepcopy(cargo)
            ccargo.rotate()
            fitr = (
                (cf, max_container, ccargo)
                for max_container in self._max_container_set
                if (cf := self._cargo_fitness(max_container, ccargo)) is not None
            )
        fit = chain(fitn, fitr)

        try:
            _, max_container, cargo = min(fit, key=lambda x: x[0])
        except ValueError:
            self.unfit_cargo_set.append(cargo)
            return None, None
        cargo.move(
            max_container.left_with_admittance + cargo.admittance,
            max_container.bottom_with_admittance + cargo.admittance,
        )
        if max_container.contains_with_admittance(cargo):
            return cargo, max_container
        return None, None

    def _split_container(
        self, max_container: Container, cargo: Cargo
    ) -> List[Container]:
        max_container_set = []

        if cargo.left_with_admittance > max_container.left_with_admittance:
            _max_container = deepcopy(max_container)
            _max_container.length = max_container.left - cargo.left
            max_container_set.append(_max_container)
        if cargo.right_with_admittance < max_container.right_with_admittance:
            _max_container = deepcopy(max_container)
            _max_container.length = max_container.right - cargo.right
            _max_container.x = cargo.right
            max_container_set.append(_max_container)
        if cargo.top_with_admittance < max_container.top_with_admittance:
            _max_container = deepcopy(max_container)
            _max_container.width = max_container.top - cargo.top
            _max_container.y = cargo.top
            max_container_set.append(_max_container)
        if cargo.bottom_with_admittance > max_container.bottom_with_admittance:
            _max_container = deepcopy(max_container)
            _max_container.width = max_container.bottom - cargo.bottom
            max_container_set.append(_max_container)

        return max_container_set

    def _split_containers(self, cargo: Cargo) -> None:
        max_container_set = list()
        for container in self._max_container_set:
            if container.intersects_with_admittance(cargo):
                max_container_set.extend(self._split_container(container, cargo))
            else:
                max_container_set.append(container)
        self._max_container_set = list(max_container_set)

    def _remove_duplicates(self):
        contained = set()
        for m1, m2 in itertools.combinations(self._max_container_set, 2):
            if m1.contains(m2):
                contained.add(m2)
            elif m2.contains(m1):
                contained.add(m1)

        self._max_container_set = [
            m for m in self._max_container_set if m not in contained
        ]

    def fitness(
        self, cargo: Cargo
    ) -> Union[Tuple[Cargo, Container], Tuple[None, None]]:
        cargo, max_container = self._select_position(cargo)
        if cargo is None:
            return None, None
        return cargo, max_container

    def add_cargo(self, cargo: Cargo) -> None:
        cargo, _ = self._select_position(cargo)
        if not cargo:
            return None
        self._split_containers(cargo)
        self.cargo_set.append(cargo)
        self._remove_duplicates()
        self.container.weight_left -= cargo.weight

    def add_cargo_set(self, cargo_set: List[Cargo]) -> None:
        cargo_set = deepcopy(cargo_set)
        cargo_set = sorted(cargo_set, key=lambda c: c.weight_per_area, reverse=True)
        for cargo in cargo_set:
            self.add_cargo(cargo)
        self.validate_packing()
