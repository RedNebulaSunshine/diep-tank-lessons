---
title: A hand that follows the cursor
summary: An auto turret with Range 0 that aims with the cursor rests at its Facing, swings to the cursor while you hold fire, and drops back when you let go.
pack: lesson-07-hand
tank: Waver
---

## What you see

An arm holding a wand. At rest it hangs to the side; hold fire and it reaches toward the cursor; let go and it drops back. Every held thing in our packs works this way: wands, scythes, wrenches, candy bags, thrown bats.

## The trick

!chalk(07-hand)

Two settings on one auto turret. **Range 0** so it never looks for enemies, and **Aims with the cursor (Auto Smasher)** on so the player steers it. With both, the turret rests at its **Facing** until the fire button is held, then turns to the cursor inside its **Arc**, and returns to rest on release. What it carries makes no difference: a bare rod, a drawn hand, even a gun.

```scene
{"steps": [
 {"show": ["cannon"], "focus": "Tank body", "say": "A plain tank."},
 {"show": ["cannon", "arm pivot"], "focus": "arm pivot", "say": "An auto turret at **Offset X −10, Offset Y 44**: **Range 0**, **Aims with the cursor** on, **Facing 35**, **Arc 70**. **Base size 8** and **Same color as the body** make the disc a shoulder joint."},
 {"show": ["cannon", "arm pivot", "arm"], "focus": "arm", "say": "The arm is a barrel riding the pivot: **Length 60**, **Width at base 0.38×**, **Fires: Nothing**, **Same color as the body**."},
 {"show": ["cannon", "arm pivot", "arm", "hand", "wand", "wand star"], "focus": "wand", "say": "A Yellow circle for the hand, a Brown barrel for the wand and a star at its tip all ride the same pivot and turn with it."},
 {"live": true, "say": "**Play.** Hold fire and move the cursor: the hand follows. Let go: it drops back to rest."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Range | 0 | Any other value makes it track enemies as well (lesson 09) |
| Aims with the cursor | on | Off, it is a fixed prop |
| Facing | 35 | The rest pose. 0 reads as "always points at the cursor", since the body does too |
| Arc | 70 | Always set one: a pivot with Arc 0 wanders when released |
| Base size | 8 | Small enough to read as a joint |

## Gotchas

- It follows the cursor only while the cursor is **inside its wedge** (Facing ± Arc). An arm resting backward never reaches a forward cursor.
- A gun that **Fires on right click** mounted on such a pivot never fires at all. Put that gun on the body instead, invisible, where the held item rests, and keep the drawing on the pivot.
- A gun that fires on the left button works fine on the pivot and aims with it: a wand that shoots stars.

## Where we used it

::: seen
![Babayaga: the wand arm](img/halloween-babayaga.png)
![Reaper: the scythe hand](img/halloween-reaper.png)
![Stitches: a wrench arm](img/halloween-stitches.png)
:::
