import pytest
from packer import Kuzov


@pytest.fixture()
def gazelle() -> Kuzov:
    return Kuzov(
        length=3090,
        width=2078,
        height=2000,
        weight=1320,
    )
