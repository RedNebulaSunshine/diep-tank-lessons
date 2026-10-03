---
title: Jaws that bite
summary: Two cursor pivots resting apart swing together when you hold fire, and invisible barrels along the jaws hurt whatever is caught between them.
pack: lesson-08-jaws
tank: Chomper
---

## What you see

A mouth that hangs open, snaps shut while you hold fire, and bites what is inside it.

## The trick

Two of lesson 07's pivots, one each side of the aim, resting at **Facing ±45** so the mouth is open. Hold fire and each pivot turns toward the cursor from its own spot, so both bars swing inward and meet. Release and they fall open again.

The bite is three **invisible** barrels along the inside of each jaw that fire a stationary, short-lived bullet with **Always fire** on: a damage point that hurts anything touching it. Whatever sits between the closed jaws takes six bites a second.

```scene
{"live": {"enemy": true}, "steps": [
 {"show": ["jaw pivot right"], "focus": "jaw pivot right", "say": "A cursor pivot (**Range 0**, **Aims with the cursor** on) at **Offset X 40, Offset Y 20**, resting at **Facing 45** with **Arc 60**. **Base size 10**, **Same color as the body**."},
 {"show": ["jaw pivot right", "jaw right bar"], "focus": "jaw right bar", "say": "The jaw: a barrel riding the pivot, **Length 140**, **Fires: Nothing**, **Same color as the body**."},
 {"show": ["jaw pivot right", "jaw right bar", "jaw right tooth 1", "jaw right tooth 2", "jaw right tooth 3", "jaw right tooth 4", "jaw right fang"], "focus": "jaw right fang", "say": "Teeth are triangle parts riding the same pivot, pointing inward; the fang is a hooked one at the tip."},
 {"show": ["jaw pivot right", "jaw right bar", "jaw right tooth 1", "jaw right tooth 2", "jaw right tooth 3", "jaw right tooth 4", "jaw right fang", "jaw right bite 1", "jaw right bite 2", "jaw right bite 3"], "focus": "jaw right bite 2", "say": "Three **invisible** barrels along the inside: **Always fire**, **Bullet speed 0**, **Launch speed 0**, **Lifetime 0.2**, **Penetration 20**, **Reload 0.5**. Each drops a tiny bullet where it is. The editor shows invisible barrels faded."},
 {"show": ["jaw pivot right", "jaw right bar", "jaw right tooth 1", "jaw right tooth 2", "jaw right tooth 3", "jaw right tooth 4", "jaw right fang", "jaw right bite 1", "jaw right bite 2", "jaw right bite 3", "jaw pivot left", "jaw left bar", "jaw left tooth 1", "jaw left tooth 2", "jaw left tooth 3", "jaw left tooth 4", "jaw left fang", "jaw left bite 1", "jaw left bite 2", "jaw left bite 3"], "focus": "jaw pivot left", "say": "Mirror the lot (**Flip horizontal**): the left pivot rests at **Facing −45**."},
 {"show": "all", "focus": "eye left", "say": "Two eyes from lesson 05 finish the face."},
 {"live": true, "say": "**Play.** Hold fire with the cursor ahead: both bars swing to it and the mouth closes. Release: it falls open."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Facing | ±45 | How wide the mouth hangs open |
| Arc | 60 | Must be at least the rest angle, or the jaws can never meet (30 left a test stuck 15° open) |
| Bite points | 3 per jaw | Along the inside edge; each is a firing barrel against the budget |
| Bite Lifetime | 0.2 s | Short, so the points do not pile up |
| Penetration | 20 | Keeps the bite alive through a hit so it keeps biting |

## Gotchas

- Six always-firing bite points are a noticeable slice of the lobby's 120-a-second budget; lesson 15 shows how to see the number before importing.
- The jaws are a picture: only the bite points do damage. Teeth that are parts do not hurt (unless you tick **Collidable**, lesson 12).
- Both pivots count toward the eight auto turrets, with the eyes that is four.

## Where we used it

::: seen
![Nandor: a bite zone in front of the face on a pivot](img/halloween-nandor.png)
![Dracula: the same bite, bigger](img/halloween-dracula.png)
:::
