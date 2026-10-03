"""Lesson 02: drawing with barrels: hair-thin lines, a barrel that crosses the centre, needles and fans."""
from _common import C, run


def build(p):
    d = p.tank("Line art", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(length=80, name="cannon")
    d.line((24, -32), (32, -10), width=5, color=C.charcoal, name="brow left")
    d.line((24, 32), (32, 10), width=5, color=C.charcoal, name="brow right")
    d.rod_polar(angle=-40, length=140, gap=-70, width=5, color=C.charcoal, above=True, name="scar (Gap -70)")
    d.rod((30, 0), (125, 0), width=18, end_width=1, color=C.white, name="horn (tip 0.02 wide)")
    d.rod((-20, 0), (-110, 0), width=8, end_width=46, color=C.white, name="fan tail (tip 1.1 wide)")
    return d


if __name__ == "__main__":
    run(build, "Lesson 02 Line art")
