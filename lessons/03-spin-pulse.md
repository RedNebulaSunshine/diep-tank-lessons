---
title: Spinning parts and a pulsing light
summary: Spin speed turns a part on its own, and two stars spinning against each other read as a light that pulses.
pack: lesson-03-spin-and-pulse
tank: Lantern
---

## What you see

A gear that turns and a lantern that pulses. Neither fires anything, and neither costs a barrel: they are plain parts with **Spin speed** set.

## The trick

!chalk(03-spin-pulse)

**Spin speed** on a part is rotation per tick, 25 ticks a second: 0.05 is about one turn every five seconds, 0.5 is the slider's end. The editor's preview does not animate, so you only see it in play.

The pulse is a discovery a skill user sent in: put **two star parts on the same spot**, a bigger darker one under a smaller lighter one of the same hue, and give them **equal and opposite Spin speed**. When their spokes line up they look like one bright star; half a spoke later they interleave into a dimmer, rounder blob. The eye reads it as a light beating.

```scene
{"steps": [
 {"show": ["cannon"], "focus": "Tank body", "say": "A plain tank. Everything here is a part, so no barrels and no budget."},
 {"show": ["cannon", "gear", "gear hub"], "focus": "gear", "say": "The gear: an 8-point star (**Sides 8**, **Drawn as a star**) of **Size 28**, **Spin speed 0.05**. A Charcoal hub on top hides its centre."},
 {"show": ["cannon", "gear", "gear hub", "lantern pole"], "focus": "lantern pole", "say": "A pole: a Brown barrel, **Fires: Nothing**, out to the tank's right."},
 {"show": ["cannon", "gear", "gear hub", "lantern pole", "lantern back"], "focus": "lantern back", "say": "The lantern's back star: 3 spokes, Orange, **Size 21.6**, **Spin speed −0.05**, over the body."},
 {"show": ["cannon", "gear", "gear hub", "lantern pole", "lantern back", "lantern front"], "focus": "lantern front", "say": "The front star: 3 spokes, Yellow, **Size 18**, same **Offset**, **Spin speed +0.05**. Aligned they are one bright star; interleaved, a dim disc. It beats about once a second."},
 {"live": true, "say": "**Play.** The gear turns, the lantern pulses, and the tank is otherwise unchanged."}
]}
```

## Numbers that matter

| Spokes | Spin speed | Beat |
|---|---|---|
| 3 | ±0.05 | about once a second: a lantern, a heartbeat |
| 3 | ±0.12 | a flicker |
| 6 | ±0.05 | twice a second |

Beat period in seconds is (360° ÷ spokes) ÷ (2 × spin × 25 × 57.3). Three or six spokes read as light; four looks mechanical.

## Gotchas

- Both stars need exactly the same **Offset X** and **Offset Y**, and the smaller one must be the higher layer.
- Give the stars their own colours. On Team color the pulse would change with the team.
- **Auto rotate** under Movement and durability spins the body itself; the barrels and your aim stay put.

## Where we used it

::: seen
![Troublemaker: a propeller beanie on Spin speed](img/halloween-troublemaker.png)
![Frankensmash: spinning head bolts](img/halloween-frankensmash.png)
:::
