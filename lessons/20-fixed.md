---
title: A part that keeps its heading
summary: A part's Rotation can be Fixed. It then holds its angle in the world while the tank turns, like a dominator's base or a compass needle.
pack: lesson-20-fixed
tank: Navigator
---

## What you see

A round tank on a dark square plinth, with a red needle across its middle. Aim anywhere: the cannon turns, the body turns, and the square and the needle stay exactly as they were, like the base of a Dominator.

## The trick

!chalk(20-fixed)

The editor update of 6 October 2026 turned a part's old **Spin speed** field into a **Rotation** choice with three settings: **With the aim** (the usual: the part turns with the tank), **Spins** (turns on its own; the speed box appears) and **Fixed**. A Fixed part keeps its **Angle in the world** instead of following the aim. That is the whole trick.

```scene
{"steps": [
 {"show": ["base (fixed)"], "focus": "base (fixed)", "say": "A Charcoal square of **Size 82** at **Offset 0, 0**, under the body, with **Rotation: Fixed**."},
 {"show": ["base (fixed)", "cannon"], "focus": "cannon", "say": "A stock cannon. It turns with the aim, as barrels always do."},
 {"show": "all", "focus": "needle (fixed)", "say": "A Crimson triangle of **Size 32** over the body, **Rotation: Fixed**, and a small hub to hide its pivot. The needle points one way on the map, whatever the tank does."},
 {"live": true, "say": "**Play** and move the mouse around the tank: the cannon follows, the square and the needle hold still."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Rotation | Fixed | One of three: With the aim, Fixed, Spins. A part cannot be fixed and spin |
| Offset X, Offset Y | 0, 0 | Only the **angle** is fixed. A part placed off-centre still swings round the tank's centre as you aim |
| Angle | a direction on the map | Measured in the world, not from the aim: try it in the real editor to see which way 0 points |

## Gotchas

- **Only the angle is fixed.** A fixed square at Offset X 60 keeps its corners pointing the same way but still orbits the body as the tank turns. Put fixed parts at the centre, or accept the swing.
- The editor's preview does not animate, so a Fixed part looks like any other there. Press Play.
- Everything riding a fixed part (lesson 19) stays fixed with it: a fixed hub with riders is a map-aligned frame to hang things on.

## Where to use it

A dominator or a turret base; a compass needle on a navigator or an explorer; a shadow under a figure; a crown or a hat that stays upright while a face turns under it; a square frame that makes a round tank read as a crate or a tile.
