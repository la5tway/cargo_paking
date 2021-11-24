import itertools
from copy import deepcopy
from itertools import chain
from typing import List, Tuple, Union

from cargo import Cargo
from kuzov import Kuzov


class Scheduler:
    def __init__(
        self,
        kuzov: Kuzov,
        rotate: bool = False,
    ) -> None:
        self.kuzov = deepcopy(kuzov)
        self.rotate = rotate
        self.cargo_set: list[Cargo] = []
        self.unfit_cargo_set = []
        self._max_kuzov_set = [deepcopy(kuzov)]

    def used_area(self) -> float:
        return sum(cargo.area_with_admittance for cargo in self.cargo_set)

    def validate_packing(self):
        kuzov = deepcopy(self.kuzov)
        for cargo in self.cargo_set:
            if not kuzov.contains_with_admittance(cargo):
                raise Exception("Cargo placed outside kuzov")

        len_cargo_set = len(self.cargo_set)
        if len_cargo_set <= 1:
            return

        for c1 in range(0, len_cargo_set - 2):
            for c2 in range(c1 + 1, len_cargo_set - 1):
                if self.cargo_set[c1].intersects_with_admittance(self.cargo_set[c2]):
                    raise Exception("Cargo collision detected")

    def _cargo_fitness(self, max_kuzov: Kuzov, cargo: Cargo):
        if (
            cargo.width_with_admittance <= max_kuzov.width
            and cargo.length_with_admittance <= max_kuzov.length
        ):
            if cargo.weight <= self.kuzov.weight_left:
                return max_kuzov.left_with_admittance
        return None

    def _select_position(
        self, cargo: Cargo
    ) -> Union[Tuple[Cargo, Kuzov], Tuple[None, None]]:
        if not self._max_kuzov_set:
            return None, None

        fitn = (
            (cf, max_kuzov, cargo)
            for max_kuzov in self._max_kuzov_set
            if (cf := self._cargo_fitness(max_kuzov, cargo)) is not None
        )
        fitr = []
        if self.rotate:
            ccargo = deepcopy(cargo)
            ccargo.rotate()
            fitr = (
                (cf, max_kuzov, ccargo)
                for max_kuzov in self._max_kuzov_set
                if (cf := self._cargo_fitness(max_kuzov, ccargo)) is not None
            )
        fit = chain(fitn, fitr)

        try:
            _, _max_kuzov, _cargo = min(fit, key=lambda x: x[0])
        except ValueError:
            self.unfit_cargo_set.append(cargo)
            return None, None
        _cargo.x = _max_kuzov.left_with_admittance + _cargo.admittance
        _cargo.y = _max_kuzov.bottom_with_admittance + _cargo.admittance
        return _cargo, _max_kuzov

    def _split_kuzov(self, max_kuzov: Kuzov, cargo: Cargo) -> List[Cargo]:
        max_kuzov_set = []

        if cargo.left_with_admittance > max_kuzov.left_with_admittance:
            _max_kuzov = deepcopy(max_kuzov)
            _max_kuzov.length = max_kuzov.left - cargo.left
            max_kuzov_set.append(_max_kuzov)
        if cargo.right_with_admittance < max_kuzov.right_with_admittance:
            _max_kuzov = deepcopy(max_kuzov)
            _max_kuzov.length = max_kuzov.right - cargo.right
            _max_kuzov.x = cargo.right
            max_kuzov_set.append(_max_kuzov)
        if cargo.top_with_admittance < max_kuzov.top_with_admittance:
            _max_kuzov = deepcopy(max_kuzov)
            _max_kuzov.width = max_kuzov.top - cargo.top
            _max_kuzov.y = cargo.top
            max_kuzov_set.append(_max_kuzov)
        if cargo.bottom_with_admittance > max_kuzov.bottom_with_admittance:
            _max_kuzov = deepcopy(max_kuzov)
            _max_kuzov.width = max_kuzov.bottom - cargo.bottom
            max_kuzov_set.append(_max_kuzov)

        return max_kuzov_set

    def _split(self, cargo: Cargo) -> None:
        max_kuzov_set = list()
        for kuzov in self._max_kuzov_set:
            if kuzov.intersects_with_admittance(cargo):
                max_kuzov_set.extend(self._split_kuzov(kuzov, cargo))
            else:
                max_kuzov_set.append(kuzov)
        self._max_kuzov_set = list(max_kuzov_set)

    def _remove_duplicates(self):
        contained = set()
        for m1, m2 in itertools.combinations(self._max_kuzov_set, 2):
            if m1.contains(m2):
                contained.add(m2)
            elif m2.contains(m1):
                contained.add(m1)

        self._max_kuzov_set = [m for m in self._max_kuzov_set if m not in contained]

    def fitness(self, cargo: Cargo) -> Union[Tuple[Cargo, Kuzov], Tuple[None, None]]:
        cargo, max_kuzov = self._select_position(cargo)
        if cargo is None:
            return None, None
        return cargo, max_kuzov

    def add_cargo(self, cargo: Cargo) -> None:
        cargo, _ = self._select_position(cargo)
        if not cargo:
            return None
        self._split(cargo)
        self.cargo_set.append(cargo)
        self._remove_duplicates()
        self.kuzov.weight_left -= cargo.weight

    def add_cargo_set(self, cargo_set: List[Cargo]) -> None:
        cargo_set = deepcopy(cargo_set)
        cargo_set = sorted(cargo_set, key=lambda c: c.weight_per_area, reverse=True)
        for cargo in cargo_set:
            self.add_cargo(cargo)
        self.validate_packing()
