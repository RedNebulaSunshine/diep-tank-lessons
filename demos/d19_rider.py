"""Lesson 19: a part that rides a part: moons riding a spinning planet orbit it, and guns riding a
spinning plate turn with it and fire (the game's "rotating gun ring")."""
from _common import C, run


def build(p):
    d = p.tank("Orrery", level=1, parents=[0])
    d.hull(0, 50)
    plate = d.shape(8, 64, color=C.charcoal, name="plate")                 # the carrier; gun_ring() spins it
    d.gun_ring(plate, n=2, radius=40, length=62, auto_fire=True, above=True, spin=0.02, name="ring gun")  # above: over the plate, not under it
    planet = d.shape(0, 26, at=(-112, 0), color=C.periwinkle, name="planet")  # a second carrier, clear of the hull
    d.orbit(planet, n=3, radius=44, size=8, color=C.yellow, spin=0.04, name="moon")
    d.cannon(name="cannon")
    d.set(helpText="The moons go round; the ring guns turn and fire")
    return d


if __name__ == "__main__":
    run(build, "Lesson 19 Rider")
