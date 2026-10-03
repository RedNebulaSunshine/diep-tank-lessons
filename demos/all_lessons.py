"""Every lesson's demo tank in one pack."""
import importlib
from _common import run

MODULES = ["d00_layers", "d01_face", "d02_line_art", "d03_spin_pulse", "d04_pistons", "d05_eyes",
           "d06_tail", "d07_hand", "d08_jaws", "d09_limbs", "d10_trail", "d11_dash", "d12_hitbox",
           "d13_shots", "d14_ghost"]


def build(p):
    for k, m in enumerate(MODULES):
        d = importlib.import_module(m).build(p)
        # The stock Tank already offers 6 upgrades and the engine allows 19 per tank, so the
        # last two lesson tanks hang off Twin (1) in the all-in-one pack. Play reaches any of them.
        if k >= 13:
            d.parents = [1]


if __name__ == "__main__":
    run(build, "Tank lessons")
