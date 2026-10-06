---
title: A part that rides a part
summary: Since the October 2026 update a part or a barrel can sit on another part. Spin the carrier and everything riding it goes round: moons, a lantern wheel, a chained tail, a gun ring that turns and fires.
pack: lesson-19-rider
tank: Orrery
---

## What you see

A dark plate turns slowly under the body with two guns riding it, so the guns sweep round and fire as they go. Behind the tank a small planet spins with three yellow moons circling it. Nothing here is a turret or a drone: it is parts riding parts.

## The trick

!chalk(19-rider)

Before the update a part could ride a barrel or an auto turret, and that was all (lessons 05 to 09 are built on riding turrets). The editor update of 6 October 2026 added **Rides on** for parts: a part, or a barrel, can ride another **part**. Its **Offset X**, **Offset Y** and **Angle** are then measured from the carrier's centre, along the carrier's angle. Give the carrier **Rotation: Spins** and everything riding it orbits. A barrel that rides a part turns with it **and still fires**, which is how the game's change notes describe "a rotating gun ring".

```scene
{"steps": [
 {"show": ["plate"], "focus": "plate", "say": "The carrier: an octagon of **Size 64** in Charcoal, under the body, with **Rotation: Spins** at **Spin speed 0.02**: one turn in about 13 seconds."},
 {"show": ["plate", "ring gun 1", "ring gun 2"], "focus": "ring gun 1", "say": "Two barrels with **Rides on: plate**, **Gap 40** so they start outside the plate's middle, at **Angle 0** and **180**, on **Always fire**. They draw over the plate (a rider draws under its carrier unless you put it over) and turn with it."},
 {"show": ["plate", "ring gun 1", "ring gun 2", "planet"], "focus": "planet", "say": "A second carrier: a Periwinkle circle of **Size 26** at **Offset X −112**, **Rotation: Spins** at **0.04**."},
 {"show": "all", "focus": "moon 1", "say": "Three Yellow circles of **Size 8** with **Rides on: planet**, at **Offset X 44** and **Angle 0, 120, 240** from the planet's centre, placed over it. Every one of them is **looks only**: a riding part has no hitbox."},
 {"live": true, "say": "**Play.** The moons go round the planet, the guns sweep round the plate and fire where they point. Steer: the whole orrery turns with the tank and keeps spinning."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Carrier Spin speed | 0.02 to 0.05 | Rotation per tick; 0.02 is a turn in about 13 s, 0.05 one in 5 s |
| Rider Offset X | the orbit radius | Measured from the carrier's centre, along the carrier's angle |
| Rider Angle | 0, 120, 240 | Spaces riders evenly; the carrier's spin is added to all of them |
| Chain depth | 4 at most | A root part and four riders in a line; the editor clears a deeper link |
| Riders' hitbox | none | The import clears **Collidable** on a rider; tick it on the carrier instead |

## Gotchas

- **A rider draws under its carrier** unless you place it over (the same rule as a part on a barrel). Moons under their planet are barely visible; the first version of this demo had exactly that problem.
- **Rides on one thing.** A part that rides a barrel or an auto turret cannot also ride a part; the editor keeps the barrel first, the turret second, the part third.
- **The editor's tooltip on a riding barrel says "Looks only; it fires nothing".** It does fire (seen in play, 6 October 2026). Give it **Always fire** if the ring should spray on its own.
- Nothing bends. A chained tail of riders turns as one piece when the root spins; for a tail that lags turns see lesson 06.
- The carrier can itself ride a turret or a barrel, so a spinning wheel can hang off a swinging arm.

## Where to use it

Moons and electrons; a clock (two riders of different lengths on a slow hub, or two hubs at different speeds); lanterns, bells or gondolas on a wheel; a halo of motes that costs no budget because they are parts, not drones; an eye whose pupil rides the eyeball; and a gun ring that sprays as it turns.
