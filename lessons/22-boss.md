---
title: A boss of your own
summary: A pack can now spawn bosses. A boss is a record in the Bosses tab that wraps one of your tanks: a size, a health bar, a brain, a behaviour, a spawn ring. Here is one, and what the game does with it.
pack: lesson-22-boss
tank: Warden
---

## What you see

A grey three-horned tank with a drone spawner at the back and a big gun in front. On its own it is a tank nobody can pick: it is not in the class tree. In a lobby with this pack loaded, the arena announces **"The Warden wakes!"** and the same tank appears at two and a half times the size, with 6000 health, drifting about the inner map until a player comes within range.

## The trick

!chalk(22-boss)

The editor update of 6 October 2026 added a **Bosses** tab. A boss is two things:

1. **A tank** like any other, usually a **boss copy**: select a tank and press **Make a boss copy**. The copy is marked boss-only, so the editor drops it from the class tree and the starters, and its **Stat levels** panel is fixed at 7 for every stat (health regen 0) and read-only. You can still edit its parts and barrels, and that is where its guns, drones and hitboxes come from.
2. **A boss record** in the Bosses tab (**New boss**, or **New boss from copy**) that picks the tank and sets everything else: **Name**, **Spawn message**, **Size**, **Health**, the score it is worth, its **Brain**, what it does when it spots a player, where and how often it spawns.

The demo tank is the boss copy; the record is shown under the body in the mock inspector.

```scene
{"steps": [
 {"show": [], "focus": "Tank body", "say": "The tank: **Body size 60** in **Fallen**, the stock bosses' grey. Its **Stat levels** are fixed at 7: a boss plays maxed."},
 {"show": ["horn 1 (collidable)", "horn 2 (collidable)", "horn 3 (collidable)"], "focus": "horn 1 (collidable)", "say": "Three triangles of **Size 26** with **Collidable** on: the boss rams with them. Up to eight parts can be collidable since the update (lesson 12)."},
 {"show": ["horn 1 (collidable)", "horn 2 (collidable)", "horn 3 (collidable)", "spawner", "main gun", "side gun left", "side gun right"], "focus": "main gun", "say": "Its weapons: a wide **Length 120** cannon, two side guns at **Angle ±120**, and a rear **spawner** with 4 drones. The simple brain fires every gun it has; the drones hunt on their own."},
 {"show": "all", "focus": "Tank body", "say": "Now scroll the inspector to the **Boss** sections: the record from the Bosses tab. **Size 2.5**, **Health 6000**, **Brain: Simple**, **When it spots a player: Charge and ram** within **Spot range 2000**, **Wander around** otherwise, spawning in the inner **0 to 0.4** of the map."},
 {"live": true, "say": "**Play** drives the tank itself, at level 1 size. In the game the record takes over: the boss AI drives it at Size 2.5, and a player can press **H** to take control."}
]}
```

## The record, field by field

| Field | Warden | Notes |
|---|---|---|
| Size | 2.5 | Scales the tank and everything on it; 4 is the most. The stock bosses: Guardian 1.55, Summoner and Defender 1.72, the two Fallen 2.09, Decade 2.87 |
| Health | 6000 | Does **not** grow with Size. Stock bosses 3000, Decade 10000. A Size 4 boss at 3000 is a big soft target |
| Score for killing it | 50000 | Stock 30000, Decade 100000 |
| Brain | Simple | **Simple** drifts, rams and shoots: the stock bosses' brain. **Bot** plays the body like a sandbox bot, with a skill and a retreat threshold; in our one test it mostly wandered |
| When it spots a player | Charge and ram | Also **Stop and shoot**, **Keep distance and strafe**, **Wander and shoot at them**, or **Ignore them** (only its turrets and drones fight, the way Decade and four of the five stock bosses are built) |
| Spot range | 2000 | The most. The default form writes 1500. **A simple-brain boss fights what comes inside this range and does not hunt across the map** (seen in play, 6 October 2026), so place it where players must pass |
| When no one is near | Wander around | Or **Circle the map centre**, like the Guardian |
| Ignores players below level | 15 | The stock bosses' value; 0 attacks everyone |
| On the shapes' team | on | Bases ignore it. Off makes a Fallen-style enemy tank; a necromancer boss needs off to raise shapes |
| Spawn ring, How often | 0 to 0.4, weight 1 | The same bands as custom shapes. Weight 0 keeps it out of the rotation: it then comes only by console |

## Spawning it

- **Boss Auto-Spawn must be on** in the lobby's admin panel, or no boss ever spawns on its own. The editor warns "Boss auto-spawn is off" with a Turn on button when it is off.
- The lobby's **boss rotation** runs while the pack is loaded: by default one boss every 45 minutes, the first after 45, at most one alive. The pack can set the gap, the first delay, how many may be alive at once, and how many players must be online; it can also hide the lobby's five stock bosses or change how often each spawns, so a themed arena stays themed.
- From the console: `spawn_boss warden` (the name, lower-case, spaces removed). `set_boss <playerId> warden` turns a player into it. In the editor, **Play** can play any boss.
- A player can press **H** to take over a boss where the lobby allows it; untick **Players can take control** to keep it AI-driven.

## Gotchas

- **One tank per boss record.** The export renames every record after its tank, so two records on one tank come back with one name and `spawn_boss` cannot tell them apart. A variant boss gets its own boss copy.
- **Tune the guns in the tank, not the record.** The record sets Size, Health and body damage on touch; damage, reload and drone counts are the tank's, played at stat level 7, so a boss copy of a maxed-out tank is brutal. Our test bosses had to have their guns turned down before anyone could study them.
- Big parts, strong contrast and few colours survive the scale. Fine line art does not.
- A boss uses the same budget as any tank (lesson 15), rated at Reload level 7.
- There is one number the Bosses tab does not show: a damage floor the game writes on its own bosses (4, and 6 on Fallen Booster). A pack file can carry it (`minDamageMultiplier`), and 6 bit clearly harder in play. The form keeps it when you edit the pack.
