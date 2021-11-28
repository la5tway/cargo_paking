import pytest

from packer import Container, Cargo, render_img


@pytest.mark.unit
def test_pack_gazelle(
    gazelle: Container,
    cargo_set1: list[Cargo]
):
    render_img(gazelle, cargo_set1)
