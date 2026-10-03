---
title: A tail that swings
summary: A turret with a narrow arc, facing backward, mostly rests; when the tank turns it lags and settles back, and anything riding it swings.
pack: lesson-06-tail
tank: Swisher
---

## What you see

A tail that trails the turn and swishes back to centre. Capes, manes, broom twigs and dangling lanterns are all the same thing.

## The trick

An auto turret only moves for a target inside its wedge. Give it **Facing 180** (straight back) and a narrow **Arc** of about 20, and almost nothing ever enters that wedge, so the turret sits at rest. When the tank turns, the turret lags the body for a moment and settles back: the closest thing this editor has to something that flows. Mount the tail on it and hide the turret's grey disc under a part the same colour as the body.

```scene
{"steps": [
 {"show": ["cannon"], "focus": "Tank body", "say": "A plain tank."},
 {"show": ["cannon", "tail pivot"], "focus": "tail pivot", "say": "An auto turret at **Offset X −36**, **Facing 180**, **Arc 20**, dragged **under** the body. It only turns for a target inside that narrow wedge behind the tank, so mostly it rests."},
 {"show": ["cannon", "tail pivot", "tail"], "focus": "tail", "say": "The tail is a barrel that **rides on** the pivot: **Length 130**, tapering from **0.62×** to **0.14×**, **Fires: Nothing**, **Same color as the body**."},
 {"show": ["cannon", "tail pivot", "tail", "tail tuft"], "focus": "tail tuft", "say": "A Charcoal circle riding the same pivot, **Offset X 136**, as the tuft."},
 {"show": ["cannon", "tail pivot", "tail", "tail tuft", "tail pivot cover"], "focus": "tail pivot cover", "say": "An octagon of **Size 29** at the pivot, **Same color as the body**, hides the turret's grey disc where it pokes out from under the hull."},
 {"live": true, "say": "**Play** and swing the mouse round: the tail lags the turn and swishes back."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Facing | 180 | Away from where enemies usually are |
| Arc | 15 to 25 | Narrow enough that targets rarely pull it; 0 would let it spin freely |
| Cover | octagon Size 29 | Its inner radius (26.8) just covers a default disc of 25 |
| Base size | 25 default, or 1 | Base size 1 hides the disc without a cover |

## Gotchas

- A target inside the wedge still pulls the tail toward it, and a weapon on the pivot would fire at it. For a pure decoration that is fine.
- The tail counts as one of the tank's eight auto turrets.
- A chain of pivots does not work: a turret cannot ride a turret, so a tail bends at one joint only. For a tail that really bends, see lesson 10.

## Where we used it

::: seen
![Broomhilda: broom twigs that swing behind](img/halloween-broomhilda.png)
![Vlad: a cape hem on a rear pivot](img/halloween-vlad.png)
![Babayaga: a lantern that dangles](img/halloween-babayaga.png)
:::
