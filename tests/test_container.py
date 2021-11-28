from packer import Container


def test_intersects():
    c1 = Container(200, 200, 200, 200, x=0, y=0)
    c2 = Container(200, 200, 200, 200, x=200, y=0)
    c3 = Container(200, 200, 200, 200, x=0, y=200)
    c4 = Container(200, 200, 200, 200, x=200, y=200)

    assert not c1.intersects(c2)
    assert not c1.intersects(c3)
    assert not c1.intersects(c4)

    c2 = Container(50, 50, 200, 200, x=100, y=100)
    c3 = Container(50, 50, 200, 200, x=0, y=0)
    c4 = Container(50, 50, 200, 200, x=50, y=50)

    assert c1.intersects(c2)
    assert c1.intersects(c3)
    assert c1.intersects(c4)

    c2 = Container(200, 200, 200, 200, x=100, y=100)
    c3 = Container(200, 200, 200, 200, x=0, y=0)
    c4 = Container(200, 200, 200, 200, x=50, y=50)

    assert c1.intersects(c2)
    assert c1.intersects(c3)
    assert c1.intersects(c4)

    c2 = Container(200, 200, 200, 200, x=199, y=0)
    c3 = Container(200, 200, 200, 200, x=0, y=199)
    c4 = Container(200, 200, 200, 200, x=199, y=199)

    assert c1.intersects(c2)
    assert c1.intersects(c3)
    assert c1.intersects(c4)


def test_intersects_with_admittance():
    c1 = Container(200, 200, 200, 200, x=0, y=0)
    c2 = Container(200, 200, 200, 200, x=250, y=0)
    c3 = Container(200, 200, 200, 200, x=0, y=250)
    c4 = Container(200, 200, 200, 200, x=250, y=250)

    assert not c1.intersects_with_admittance(c2)
    assert not c1.intersects_with_admittance(c3)
    assert not c1.intersects_with_admittance(c4)

    c2 = Container(100, 100, 200, 200, x=100, y=100)
    c3 = Container(100, 100, 200, 200, x=10, y=0)
    c4 = Container(100, 100, 200, 200, x=50, y=50)

    assert c1.intersects_with_admittance(c2)
    assert c1.intersects_with_admittance(c3)
    assert c1.intersects_with_admittance(c4)

    c2 = Container(200, 200, 200, 200, x=100, y=100)
    c3 = Container(200, 200, 200, 200, x=0, y=0)
    c4 = Container(200, 200, 200, 200, x=50, y=50)

    assert c1.intersects_with_admittance(c2)
    assert c1.intersects_with_admittance(c3)
    assert c1.intersects_with_admittance(c4)
