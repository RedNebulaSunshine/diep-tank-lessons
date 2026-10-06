---
title: A missile that bursts
summary: A short barrel that fires when the missile dies is a warhead. Put that barrel on a second, short-sighted turret and the missile goes off by itself when something comes close.
pack: lesson-17-warhead
tank: Grenadier
---

## What you see

Two missiles. The first flies as a seeker (lesson 16) and bursts into ten bullets when it hits something, runs out of time or the player right-clicks. The second needs no click: it bursts on its own the moment something comes within reach, like flak.

## The warhead

!chalk(17-warhead)

A projectile's **Burst** section has three triggers: right click, getting destroyed, running out of time. Setting it off only ends the projectile; the explosion comes from barrels on it with **Fires when it bursts**, which fire once as it dies. One short barrel with a lot of **Spread** and many **Bullets per shot** is the cheap warhead; several short barrels round the bullet are the consistent one.

```scene
{"live": {"enemy": true}, "steps": [
 {"show": ["missile tube base", "missile tube"], "focus": "missile tube", "say": "The seeker tube from lesson 16, firing **Exploding missile**."},
 {"subject": "Exploding missile", "show": ["seeker", "engine"], "focus": "Projectile", "say": "The same seeker and engine. Under **Burst**, tick **Right click sets it off**, **Getting destroyed sets it off** and **Running out of time sets it off**. Setting it off ends the missile; what happens then is up to the barrels on it."},
 {"subject": "Exploding missile", "show": ["seeker", "engine", "warhead"], "focus": "warhead", "say": "The warhead: a short barrel (**Length 27**) with **Fires when it bursts**, **Bullets per shot 10**, **Spread 10**, **Bullet speed 2**, **Launch speed 1.5**, **Lifetime 0.3**, **Recoil 0**. Ten bullets in a fan the instant the missile dies."},
 {"live": true, "say": "**Play.** Fire, then right-click: every missile in the air bursts. Missiles that run out of time burst too."}
]}
```

## The proximity fuse

!chalk(17-fuse)

The game has no "explode when near" switch, but it has something as good: a gun on a projectile's turret fires by itself at whatever the turret sees. So give the missile a **second** turret with a short Range and a narrow Arc, make the warhead that turret's gun, and the missile fires its warhead the moment a target enters the small field. A long **Reload** on that gun is what stops it firing again and again.

```scene
{"tank": "Flak", "live": {"enemy": true}, "steps": [
 {"subject": "Flak missile", "show": ["seeker", "engine"], "focus": "seeker", "say": "The same missile and seeker. No **Burst** is needed this time."},
 {"subject": "Flak missile", "show": ["seeker", "fuse", "engine"], "focus": "fuse", "say": "The fuse: a second auto turret, **Range 400**, **Arc 80**, under the body. It only sees things close by."},
 {"subject": "Flak missile", "show": ["seeker", "fuse", "engine", "warhead"], "focus": "warhead", "say": "The warhead now **rides on** the fuse as its gun: **Invisible**, **Length 68**, **Gap −81** so it lies across the missile, the same ten-bullet fan, and **Reload 20**. A gun on a projectile's turret fires on its own at what the turret sees, and the long reload makes that about once per missile."},
 {"live": true, "say": "**Play.** Fire past the square: when a missile comes within 400 of it, the fuse sees it and the warhead goes off."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Warhead Length | 27 | Very short, or the barrel pokes through the target and fires behind it |
| Bullets per shot, Spread | 10, 10 | One barrel, a wide fan. Several accurate barrels give a full circle but cost more entities |
| Bullet speed, Launch speed | 2, 1.5 | How fast the burst expands |
| Warhead Lifetime | 0.3 s | How far it reaches; short is cheap in the budget |
| Fuse Range, Arc | 400, 80 | The small field that sets it off. Keep the Arc at 80 or under: a wide fuse misfires |
| Fuse gun Reload | 20 | The rate limiter: about one blast per missile |

## Gotchas

- Bullets and traps work as a warhead. Drones only work on a right-click payload (**Fires on right click** instead of **Fires when it bursts**) on a missile that stays alive.
- The player who sent this could not get a warhead to work when mounted on the **seeker** turret itself. Keep it on the bullet, or on its own fuse turret.
- A Burst with nothing marked **Fires when it bursts** just ends the missile: on the Flak missile a right-click trigger would be a self-destruct, nothing more.
- The fuse gun counts once per live missile in the budget, like the engine; at Reload 20 that is almost nothing.

The [guide to creating missiles](missile-guide.html) is a write-up supplied by Random Troller, the author of the seeking projectile technique.
