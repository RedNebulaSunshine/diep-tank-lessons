---
title: A dash on right click
summary: An invisible barrel pointing backward fires a harmless shot with huge Recoil, and the kick throws the tank forward.
pack: lesson-11-dash
tank: Pouncer
---

## What you see

Right-click and the tank lunges forward. Vampires, pouncing cats, charging bulls, fleeing thieves: all the same barrel.

## The trick

!chalk(11-dash)

Recoil pushes the tank away from the shot. So a barrel that points **backward** pushes the tank **forward**. Make it **invisible**, **Fires on right click**, with **Recoil** as high as the stock tanks go and a shot that does nothing and vanishes at once. A slow **Reload** turns it into an ability with a cooldown.

```scene
{"steps": [
 {"show": ["cannon"], "focus": "cannon", "say": "A plain tank with a cannon on the left button."},
 {"show": ["cannon", "pounce"], "focus": "pounce", "say": "The dash: an **invisible** barrel at **Angle 180** with **Gap −43** so its muzzle sits under the body. **Fires on right click**. **Recoil 16**: the kick throws the tank forward. **Damage 0**, **Penetration 0**, **Bullet speed 0**, **Launch speed 3**, **Lifetime 0.1**, **Reload 4.2**."},
 {"subject": "Dash", "show": "all", "focus": "Projectile", "say": "Its projectile is a trap drawn as a tiny star with a slow **Spin**, gone in a tenth of a second."},
 {"live": true, "say": "**Play.** Right-click (or long-press on a phone): the tank pounces. The **Tip** field says what right click does, and the game shows it to players for ten seconds."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Recoil | 16 (12 to 20 seen) | Stock recoil tops out at 17; the editor allows up to 20 |
| Reload | 4.2 | One dash every few seconds. Three dashes stacked at Reload 12 make a leap |
| Lifetime | 0.1 s | The shot must not hang around |
| Launch speed | 3 | Gets the shot clear of the body instantly |
| Tip | "Right click to dash" | Players only learn an ability if you tell them |

## Gotchas

- The shot still costs budget each time, but at Reload 4.2 that is almost nothing.
- Recoil also applies on the left button: a big front-facing cannon with high Recoil walks the tank backward, which is how the stock Booster and Rocketeer work.
- Put nothing between the muzzle and the body: the shot spawns at the muzzle and a part there would catch it.

## Where we used it

::: seen
![Nandor: a lunge on the right button](img/halloween-nandor.png)
![Stitches: a RAGE charge](img/halloween-stitches.png)
:::
