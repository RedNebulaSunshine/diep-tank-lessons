---
title: A salvo that fans out
summary: Six missiles leave the tube as one, a sideways recoil barrel kicks them apart a moment later, and each bursts when it dies. The missiles are drones, which is what makes the volley affordable.
pack: lesson-18-cluster
tank: Volley
---

## What you see

Hold fire and a tight bundle of missiles leaves the tank, splits into a spreading fan a moment later, and each one bursts into shards when it runs out of time. A cluster rocket, a volley of arrows, a swarm of darts.

## The trick

!chalk(18-cluster)

Nothing in this game splits in flight: a shot fired by a projectile is always a plain one (lesson 13). So the salvo is fired all at once, and the "split" is a **splitter** on each missile: a sideways barrel with the most **Recoil** and **Spread** the editor allows, firing a harmless speck a tenth of a second after launch. Each missile is kicked off the line in its own direction. Six missiles from one barrel would blow the per-second budget as bullets, so the missiles are **drones**: drones count against the drone limit and the room, not per second.

```scene
{"steps": [
 {"show": ["cluster tube 1", "cluster tube 2"], "focus": "cluster tube 1", "say": "Two stock-length barrels on the same spot, each with **Fires: Cluster missile** (1 and 2), **Bullets per shot 6**, **Spread 0**, **Recoil 0**, **Knockback 0**, **Reload 6**, **Lifetime 3**, **Max drones 2**. Spread and Knockback must be 0 or the bundle drifts apart before the splitters act."},
 {"subject": "Cluster missile 1", "show": [], "focus": "Projectile", "say": "**Based on** Drone, shape **Its own**, **Sides 0** (round). Under **Burst**, all three triggers on."},
 {"subject": "Cluster missile 1", "show": ["warhead"], "focus": "warhead", "say": "The warhead from lesson 17: **Fires when it bursts**, **Bullets per shot 4**, **Spread 10**, **Bullet speed 2**, **Launch speed 1.5**, **Lifetime 0.3**."},
 {"subject": "Cluster missile 1", "show": ["warhead", "splitter"], "focus": "splitter", "say": "The splitter: an **invisible** barrel at **Angle 90** (−90 on Cluster missile 2), **Recoil 20**, **Spread 20**, **Reload 20**, **Delay 0.1**, firing a harmless 0.1 s speck. No flag on it: a plain barrel on a drone fires while its owner holds fire. A moment after launch it kicks the missile sideways, a different way each time."},
 {"subject": "Cluster missile 1", "show": ["warhead", "splitter", "tail"], "focus": "tail", "say": "The tail is a drawn barrel (**Fires: nothing**) at Angle 180 in the body colour, so the salvo looks like rockets."},
 {"live": true, "say": "**Play** and keep the button down: six missiles leave as one, split apart, and burst as they time out."}
]}
```

## Setting bullets per shot on a drone barrel

Once a barrel fires a drone, the editor's form hides **Bullets per shot**, **Spread**, **Recoil** and **Launch speed**. The fields are still there: set them while the projectile is still **Based on** Bullet, then switch it back to Drone. The pack keeps the numbers (the editor's import and export both carry them) and the game obeys them, so one barrel fires six drones at once with no spread. A pack written by hand or by a script simply writes the fields.

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Tube Bullets per shot | 6 | Six missiles per pull; two tubes make twelve |
| Tube Spread, Recoil, Knockback | 0 | The bundle must stay together until the splitters fire |
| Tube Reload, Lifetime | 6, 3 s | A salvo every few seconds; the missiles burst when they time out |
| Splitter Recoil, Spread | 20, 20 | The editor's maximum for both; that is what fans the salvo out |
| Splitter Delay | 0.1 | In reload periods: with Reload 20 it fires about a second out |
| Volley | 58 of 64 | Two tubes × six missiles × (one missile + four shards + the speck). The lobby refuses more than 64 entities per pull |

## Gotchas

- **Hold left click after firing.** The splitters are plain barrels on a drone, and those fire only while the owner is firing. Let go at once and the bundle never splits.
- The limit here is the 64 per volley, not the per-second budget. More missiles means fewer shards each.
- One tube gives a one-sided fan; the second tube with the opposite splitter angle gives the other side. Same spot, same reload, so they fire together.
- What **Max drones 2** does when six are fired per shot is not pinned down; the sample pack ships with 2 and works.
