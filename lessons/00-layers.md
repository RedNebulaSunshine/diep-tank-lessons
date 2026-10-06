---
title: How the editor draws a tank
summary: Barrels, parts and auto turrets are stacked in layers, and the body splits what draws over it from what draws under it.
pack: lesson-00-layers
tank: Layers
---

## What you see

!chalk(00-layers)

Every custom tank is a **body** plus a stack of layers. The **Layers** panel on the left lists them; the **Tank body** row in the middle of the list splits what draws **over** the body from what draws **under** it. Drag a layer across that row and it changes sides. Within each side, the layer higher in the list is painted on top.

There are three kinds of layer, and that is all there is:

| Layer | What it is | Fields that place it |
|---|---|---|
| **Barrel** | A rectangle or trapezoid that can fire. The only straight-edged shape you get. | Angle, Offset, Length, Width at base, Width at tip, Gap |
| **Part** | A regular polygon, a circle (**Sides** under 3) or a star. | Sides, Size, Angle, Offset X, Offset Y |
| **Auto turret** | A disc that turns on its own, and carries barrels and parts with it. | Offset X, Offset Y, Base size, Facing, Range, Arc |

```scene
{"steps": [
 {"show": [], "focus": "Tank body", "say": "Every tank starts as a **body**: a circle of **Body size** 50 in the **Team color**. Blue to you, red to everyone else."},
 {"show": ["plate (under the body)"], "say": "A **part** is a polygon. This one is a square of **Size** 62 (centre to corner). It sits **under** the body, so the body paints over its middle."},
 {"show": ["plate (under the body)", "cannon"], "focus": "cannon", "say": "A **barrel** is the only rectangle. The stock cannon: **Length** 95, **Width at base** 1×, under the body like every stock barrel."},
 {"show": ["plate (under the body)", "cannon", "badge (over the body)"], "focus": "badge (over the body)", "say": "Drag a layer above the **Tank body** row and it draws **over** the body: this triangle sits on top of the hull."},
 {"live": true, "say": "**Play.** Hold the mouse button to fire: the cannon slides back on every shot. That slide is lesson 04."}
]}
```

## Units the editor uses

- The body is a circle of radius 50 at level 1 (**Body size**). The whole tank grows as it levels, so a maxed one is about half again that.
- A standard barrel is **Length** 95 and 42 units wide. **Width at base** and **Width at tip** are multiples of that width: 0.5 is 21 units wide, 2 is 84.
- A part's **Size** is centre to corner. A polygon **body** draws at 1.3 × its Body size (an octagon body of 44 looks like a circle of 50).
- **Angle** and **Facing** are degrees, clockwise, 0 pointing where the tank aims. **Offset X** runs along the aim, **Offset Y** across it to the tank's right.
- Everything gets a dark outline about 7.5 units wide, 72 % of its fill colour. A part under about 8 units across shows only its outline.
- **Spin speed** is rotation per tick, 25 ticks a second: 0.0628 is one turn every four seconds, and the slider stops at ±0.5.

## Gotchas

- The editor keeps **32 parts, 32 barrels and 8 auto turrets** per tank and drops the rest without a word. Everything a tank's projectiles carry counts too, up to 96 pieces in all (lesson 15).
- Name every layer (double-click it). The names in these lessons are what you will see in the real editor after importing the pack.
- **Fit** zooms the canvas to the whole tank. Holding **Shift** while dragging snaps to 10 units and 15°.
- Parts default to Border grey, barrels to Cannon grey. Every lesson says which colour it uses by the editor's swatch names.
