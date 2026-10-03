"""Lesson 09: limbs that live: controllable turrets with a rest angle, a narrow arc and a range."""
from _common import C, run


def build(p):
    d = p.tank("Scuttler", level=1, parents=[0])
    d.hull(0, 44)
    d.cannon(length=70, name="cannon")
    for side, word in ((1, "right"), (-1, "left")):
        for k, (x, ang) in enumerate([(24, 50), (-14, 105)]):
            t = d.living_limb(at=(x, 34 * side), angle=ang * side, arc=15, range=250, size=7,
                              color=C.charcoal, name=f"leg {k + 1} {word} pivot")
            knee = (58, 0)
            foot = (58 + 40 * 0.8, -40 * 0.6 * side)
            d.rod((0, 0), knee, width=12, end_width=10, color=C.charcoal, turret=t, name=f"thigh {k + 1} {word}")
            d.rod(knee, foot, width=10, end_width=6, color=C.charcoal, turret=t, name=f"shin {k + 1} {word}")
            d.shape(4, 9, at=knee, star=True, color=C.charcoal, turret=t, name=f"knee {k + 1} {word}")
    return d


if __name__ == "__main__":
    run(build, "Lesson 09 Limbs")
