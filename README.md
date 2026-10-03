# Tank lessons

How our diep.io tanks do what they do: one trick per page, each with a tiny demo tank you can
step through in a mock of the sandbox tank editor, watch move, download as a `.diep-pack`, and
pick apart in the real editor. Written for players who found the Halloween pack and asked.

**Read it:** https://rednebulasunshine.github.io/diep-tank-lessons/

| Lesson | The trick |
|---|---|
| 00 | How the editor draws a tank: layers, over and under the body, units |
| 01 | A face that keeps the team colour |
| 02 | Drawing with barrels: lines, needles, fans, crossing the centre |
| 03 | Spinning parts and a pulsing light |
| 04 | Parts that pump (wings, legs, jaws) |
| 05 | Eyes that watch |
| 06 | A tail that swings |
| 07 | A hand that follows the cursor |
| 08 | Jaws that bite |
| 09 | Limbs that live |
| 10 | A body that trails behind |
| 11 | A dash on right click |
| 12 | Hiding the body, keeping a hitbox |
| 13 | Shots that are pictures |
| 14 | Ghosts that fade |
| 15 | Staying under the lobby's budget |

## How it is built

- `lessons/*.md` is the text. Each lesson has a front matter block (title, summary, which demo
  pack and tank), Markdown, and a ```` ```scene ```` block: the step-through, as a list of
  steps naming which layers to show, which to select, and what the caption says.
- `demos/*.py` builds the demo tanks with the
  [diep-pack skill](https://github.com/RedNebulaSunshine/diep-pack-skill)'s build library
  (clone it beside this repo, or set `DIEP_PACK_SKILL` to its folder). Every part is named,
  and those names are what the editor shows after an import.
- `docs/` is the site GitHub Pages serves: `build.py` runs the demos, copies the packs and
  renders in, and turns the lessons into pages. `docs/assets/tank.js` draws a pack's JSON the
  way the editor does (a port of the skill's renderer) and sketches the moving tricks;
  `docs/assets/editor.js` is the mock of the editor's panels and the step-through.

```
python build.py              # demos + pages
python build.py --no-demos   # pages only
```

The pages need no server: open `docs/index.html` from disk and everything works.

## Corrections

If a field name, a number or a claim about the game is wrong, open an issue. The lessons
describe the editor as it was in early October 2026; the editor is a work in progress and
its labels can change.

## Licence and credits

MIT. Lessons, demo tanks and site by Sunshine ☀️ (RedNebulaSunshine). Diep.io, its tank
designs and the sandbox editor belong to the game's publisher; this project is not
affiliated with them. The living-limb, cursor-pivot, trail, dash and web techniques were
first seen in packs built by other players; the pulsing light was sent in by a user of the
skill.
