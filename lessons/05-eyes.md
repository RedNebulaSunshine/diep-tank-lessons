---
title: Eyes that watch
summary: An auto turret turns toward the nearest enemy. Make its disc the eyeball and let the pupil ride on it.
pack: lesson-05-eyes
tank: Watcher
---

## What you see

Two eyes that look at whatever comes near, pupils and all, with no gun on them.

## The trick

An **auto turret** always turns toward the nearest target inside its **Range** and **Arc**, whether or not it carries a weapon. So a turret with nothing on it but a part is a part that watches. Set the disc's **Base size** and **Base color** to make it the white of the eye, and put the pupil **on** the turret, a little ahead of its centre, so it points where the turret looks.

```scene
{"live": {"enemy": true}, "steps": [
 {"show": ["cannon"], "focus": "Tank body", "say": "A plain tank. Auto turrets draw **over** the body unless you drag them under it."},
 {"show": ["cannon", "eye left"], "focus": "eye left", "say": "Add an auto turret at **Offset X 14, Offset Y −22**: **Base size 16**, **Base color White**, **Arc 90** so it glances up to 90° either side of straight ahead, **Range** left at its default 1700."},
 {"show": ["cannon", "eye left", "eye left pupil"], "focus": "eye left pupil", "say": "The pupil is a part that **rides on** the turret: **Sides 0**, **Size 7**, **Offset X 6** from the turret's centre, drawn over the disc. Where the turret looks, so does the pupil."},
 {"show": ["cannon", "eye left", "eye left pupil", "eye right", "eye right pupil"], "focus": "eye right", "say": "The second eye is a copy at **Offset Y +22**."},
 {"live": true, "say": "**Play.** A square drifts past: both eyes follow it, and sit straight when nothing is near."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Base size | 16 (30 for a big eyeball, 1 to hide a disc) | The disc's radius |
| Base color | White | The eye's white; the pupil is Border grey |
| Arc | 90 | 0 lets it turn all the way round; a tiny arc (5) pins it |
| Range | 1700 default | 0 switches tracking off (lesson 07 uses that) |
| Pupil Offset X | 6 | Ahead of the pivot, so it reads as a glance |

## Gotchas

- A turret with nothing to shoot rests at its **Facing**: 0 looks ahead.
- Turrets cannot ride turrets: an eye on a swinging tail will not swing with it (it is placed where you put it and ignores the mount).
- Eight auto turrets per tank, and that is a hard limit. Two eyes spend two.
- Parts riding a turret can also sit under its disc (eyelids, a socket) when they are not marked over the body.

## Where we used it

::: seen
![Babayaga: eyes that track](img/halloween-babayaga.png)
![Dracula: eyes under the widow's peak](img/halloween-dracula.png)
:::
