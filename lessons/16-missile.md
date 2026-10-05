---
title: A missile that steers itself
summary: A bullet with a backward barrel on it is a rocket. Put that barrel on an auto turret and the rocket turns toward whatever the turret sees.
pack: lesson-16-missile
tank: Hornet
---

## What you see

A missile that bends toward the nearest target and runs it down. Hornets, homing spells, guided arrows, the heat seekers of a fighter jet: one projectile, two parts.

## The trick

A projectile can carry barrels (lesson 13), and a barrel with **Recoil** pushes whatever it sits on (lesson 11). So a bullet with a **backward** barrel that has **Always fire** and a lot of Recoil pushes itself along: that is how the stock Rocketeer works. Now put that engine on an **auto turret** that rides the bullet. The turret turns toward the nearest target inside its Range and Arc, the engine turns with it, and the push now points at the target.

```scene
{"live": {"enemy": true}, "steps": [
 {"show": ["missile tube base", "missile tube"], "focus": "missile tube", "say": "A Skimmer-style tube (**Reload 4**, **Bullet size 1.2**, **Lifetime 3.9**) with **Fires: Seeker missile**. Any barrel will do; the missile is the trick."},
 {"subject": "Seeker missile", "show": [], "focus": "Projectile", "say": "Under **Projectiles**: **Based on** Bullet, shape **As usual**. A missile is a bullet that carries its own engine."},
 {"subject": "Seeker missile", "show": ["engine"], "focus": "engine", "say": "The engine: a barrel at **Angle 180**, **Length 188**, **Width 2.4**, **Color: Same color as the body**, with **Always fire**. **Recoil 5** every **Reload 0.5** pushes the missile forward. Its shot does nothing: **Damage 0**, **Penetration 0**, **Bullet speed 0**, **Launch speed 0.5**, **Bullet size 0.8**, **Lifetime 0.2**."},
 {"subject": "Seeker missile", "show": ["seeker", "engine"], "focus": "seeker", "say": "The seeker: an auto turret with **Range 2000**, **Arc 25**, **Facing 0**, dragged **under** the body so its disc never shows. The engine **rides on** it, still at Angle 180: the turret turns toward the target and the recoil pushes the missile that way. Do not turn the turret round instead of the barrel."},
 {"live": true, "say": "**Play.** Fire toward the square: the missile bends toward it. Fire well away from it and the missile flies straight, because the square is outside the 25° wedge."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Engine Recoil | 5 | 3 or more to drive the missile; lower it if the launcher's own Bullet speed should carry more of the flight |
| Engine Reload | 0.5 | Short, so the push is steady. Each push costs budget, so the shot must be cheap |
| Engine Lifetime | 0.2 s | The exhaust shot must vanish at once, or it counts against the "in the air" budget |
| Engine Damage, Bullet speed | 0 | The shot is only there to kick |
| Seeker Range | 2000 | How far out the missile can see a target |
| Seeker Arc | 25 | How far either side of the launch direction it will turn |
| Turret layer | under the body | The engine barrel draws over it, so no disc shows |

## The arc is measured from where you fired

The turret's Arc is centred on the direction the missile was **fired**, not on the missile's nose as it turns. A missile with Arc 25 can only chase inside a 50° wedge from its launch line, so a target that steps out of the wedge is safe. **Only an Arc of 0 (the full circle) chases all the way round**, and a chaser needs a short Range or it locks on to whatever is behind you at launch.

Arc and Range together are the missile's **target field**. Wide and deep covers a lot of ground but picks a specific target badly; small is precise. The two shapes that work are a wide Arc with a short Range (let the engine, not the launcher's speed, do the flying) and a narrow Arc with a long Range, like the 25 and 2000 here.

## Gotchas

- Mount the engine on the turret and leave the turret at Facing 0: turn the barrel to 180, never the turret.
- The engine fires once per missile in the air, so a fast launcher costs a lot: a plain cannon at Reload 1 with this missile is 65 of the 120 a second (lesson 15). The Skimmer tube's Reload 4 brings it to 21.
- In the projectile's view the bullet counts as a body of Size 50, so the 188-long engine is also the missile's drawn tail, and it scales with the launcher's Bullet size.
- A manually guided missile is the same engine on a controllable drone: the player's cursor steers instead of the turret.

This lesson and the next two come from a write-up and a sample pack that a player of the [diep-pack skill](https://github.com/RedNebulaSunshine/diep-pack-skill) sent in. Thank you.
