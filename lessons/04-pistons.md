---
title: Parts that pump
summary: A wing or a leg that moves is a barrel firing a harmless speck, because every barrel that fires slides back on the shot.
pack: lesson-04-pistons
tank: Flapper
---

## What you see

Two wings that beat while you hold fire, one up while the other is down. There is no animation system in the editor. There is only recoil: every barrel that fires slides back along its own axis on each shot, and that slide is the whole animation.

## The trick

Draw the wing as a barrel, then make it fire something nobody will notice: a White speck with almost no damage, size or lifetime. Hold fire and the wing pumps at the barrel's reload rate. Put **Fire delay 0.5** on its partner and the pair alternates.

Two conditions, learned the hard way:

- The barrel must be at least about **0.5× wide** (22 units). A 0.3× barrel pumps so little you cannot see it, however long it is.
- Its **muzzle end must be uncovered**. The slide is along the barrel, so a part painted over the tip hides the movement, as the body hides the root. Animate the last segment of a limb, not one buried under a knee.

```scene
{"steps": [
 {"show": ["cannon"], "focus": "cannon", "say": "Any barrel that fires slides back on each shot. We are going to borrow that."},
 {"show": ["cannon", "wing right"], "focus": "wing right", "say": "Draw the wing as a barrel: **Angle 74**, **Gap 20**, **Length 137**, **Width at base 0.71×** tapering to **0.33×**, colour White."},
 {"show": ["cannon", "wing right"], "focus": "wing right", "say": "Make it fire a harmless speck: **Fires** a White bullet with **Damage 0.01**, **Penetration 0.2**, **Bullet size 0.15**, **Bullet speed 0.1**, **Lifetime 0.1**, **Recoil 0**, **Knockback 0**, **Reload 0.5**, **Spread 0**."},
 {"show": ["cannon", "wing right", "wing left"], "focus": "wing left", "say": "Copy it to the other side (**Flip horizontal**) and set **Fire delay 0.5**, so the two wings take turns."},
 {"live": true, "say": "**Play** and hold fire: the wings beat. Let go and they rest. Tick **Always fire** on both for wings that never stop."}
]}
```

## Numbers that matter

| Speck field | Value | Why |
|---|---|---|
| Damage, Penetration | 0.01, 0.2 | So it hurts nothing and dies on contact |
| Bullet size, Bullet speed, Lifetime | 0.15, 0.1, 0.1 s | A dot that vanishes at the muzzle. White specks read as sparkle |
| Recoil, Knockback | 0, 0 | So the wing beats do not push the tank around |
| Reload | 0.5 | Beat rate: lower is faster, and costs more budget |
| Fire delay | 0 and 0.5 | The pair alternates; 0.25 steps four legs round |

## Gotchas

- Every pumping part is a firing barrel and counts against the lobby's budget (lesson 15): 120 entities a second with Reload maxed. Ten pistons at Reload 0.5 can be refused. Put the **Reload** stat cap to 0 on tanks that move a lot.
- The pump only shows while the barrel fires: on click, or always with **Always fire**.
- Thin and moving are at odds. A limb is either slender and still, or about 0.5× wide and pumping.
- The speck is a real bullet for a tenth of a second; it is not drawn with the team colour because its projectile has a colour of its own (White).

## Where we used it

::: seen
![Rattlebones: a chattering jaw](img/halloween-rattlebones.png)
![Poltergeist: flailing arms and a rattling chain](img/halloween-poltergeist.png)
![Frankensmash: brows that twitch](img/halloween-frankensmash.png)
:::
