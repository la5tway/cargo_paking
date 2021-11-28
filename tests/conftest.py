import pytest
from packer import Container, Cargo


def pallet(height: int, weight: int) -> Cargo:
    return Cargo(
        length=1200,
        width=800,
        height=height,
        weight=weight,
    )


@pytest.fixture()
def gazelle() -> Container:
    return Container(
        length=3090,
        width=2078,
        height=2000,
        weight=1320,
    )


@pytest.fixture()
def fit_set_to_gazelle():
    return [
        # pallet(1500, 660),
        # pallet(1500, 950),
        # pallet(1500, 1200),
        pallet(500, 200),
        pallet(500, 200),
        pallet(500, 300),
        Cargo(500, 500, 500, 50),
        Cargo(500, 500, 500, 50),
        Cargo(600, 500, 500, 100),
        Cargo(600, 600, 500, 150),
    ]


@pytest.fixture()
def unfit_set_to_gazelle():
    return [
        pallet(1500, 1500),
        pallet(2100, 150),
        Cargo(3100, 600, 500, 150),
    ]


@pytest.fixture()
def cargo_set1(fit_set_to_gazelle, unfit_set_to_gazelle):
    return fit_set_to_gazelle + unfit_set_to_gazelle
