"""Lesson 18: a salvo that fans out: drone missiles fired six at a time, kicked apart by a
sideways recoil barrel a moment after launch, each bursting when it dies."""
from _common import C, run


def build(p):
    d = p.tank("Volley", level=1, parents=[0])
    d.hull(0, 50)
    d.set(helpText="Hold left click after firing: the salvo splits")
    d.cluster_launcher()
    return d


if __name__ == "__main__":
    run(build, "Lesson 18 Cluster")
