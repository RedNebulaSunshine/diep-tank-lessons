"""Shared setup for the lesson demos: find the diep-pack skill's build library and write packs
to ../build (copied into docs/ by build.py)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUTHOR = "☀️"   # the sun: the author name on every lesson pack


def find_skill():
    cands = [os.environ.get("DIEP_PACK_SKILL"),
             os.path.join(ROOT, "..", ".claude", "skills", "diep-pack"),
             os.path.join(ROOT, "..", "diep-pack-skill"),
             os.path.expanduser("~/.claude/skills/diep-pack")]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "scripts", "compose.py")):
            return os.path.join(c, "scripts")
    sys.exit("The diep-pack skill was not found. Clone github.com/RedNebulaSunshine/diep-pack-skill "
             "and set DIEP_PACK_SKILL to its folder.")


sys.path.insert(0, find_skill())
os.environ.setdefault("DIEP_PACK_OUT", os.path.join(ROOT, "build"))
from compose import Pack, Design, C, polar, arc, bezier  # noqa: E402,F401

TEAM = 27   # "Same color as the body": the team colour


def run(build, name):
    """Build one lesson's pack and save it (validate + render)."""
    p = Pack(name, author=AUTHOR)
    build(p)
    p.save()
    return p
