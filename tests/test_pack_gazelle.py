from typing import List

from packer import Container, Cargo, render_img


def test_pack_gazelle(
    gazelle: Container,
    cargo_set1: List[Cargo]
):
    render_img(gazelle, cargo_set1)
