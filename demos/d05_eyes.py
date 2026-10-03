"""Lesson 05: eyes that watch the nearest enemy: a turret disc with a pupil riding it."""
from _common import C, run


def build(p):
    d = p.tank("Watcher", level=1, parents=[0])
    d.hull(0, 50)
    d.cannon(length=80, name="cannon")
    d.eye(at=(14, -22), size=16, pupil=7, look=6, name="eye left")
    d.eye(at=(14, 22), size=16, pupil=7, look=6, name="eye right")
    return d


if __name__ == "__main__":
    run(build, "Lesson 05 Eyes")
