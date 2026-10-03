---
title: Hiding the body, keeping a hitbox
summary: Shrink the body to a dot and give the figure a hitbox of its own with a Collidable part.
pack: lesson-12-hitbox
tank: Shell
---

## What you see

A big armoured shell with a tiny blue dot at its heart. The dot is the body. The shell is what enemies run into.

## The trick

Only the body and parts marked **Collidable (hitbox + body damage)** collide; everything else is picture. **Body size 8** shrinks the body (and its hitbox) to a dot, so the figure can be any shape you draw. Then tick **Collidable** on the one big part that should take the hits. It collides at roughly half to two thirds of its drawn size, and it deals body damage like a hull.

```scene
{"live": {"enemy": true}, "steps": [
 {"show": [], "focus": "Tank body", "say": "**Body size 8**: the body shrinks to a dot, and so does its hitbox. It stays on **Team color**, which keeps the team rule satisfied."},
 {"show": ["cannon"], "focus": "cannon", "say": "A long cannon, **Length 110**, so it reaches out of the shell. Under the body, and drawn before the shell so the shell covers its root."},
 {"show": ["cannon", "shell (collidable)"], "focus": "shell (collidable)", "say": "An octagon of **Size 78** in Plum with **Collidable** ticked. Shapes, tanks and bullets now hit it well outside the dot, though inside its drawn rim."},
 {"show": "all", "focus": "shell top", "say": "A smaller Pink octagon on top is just drawing: no hitbox, no cost."},
 {"live": true, "say": "**Play.** The shell takes the hits; the dot in the middle is the tank's real centre."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Body size | 5 to 8 | Small enough to vanish behind the parts |
| Collidable part Size | 78 (up to 150) | Collidable parts are capped at 150 on import |
| Collidable parts | 3 at most | The editor quietly clears the flag on every later one |
| Contact edge | about 0.5 to 0.67 × Size | Measured in play with rings of dots; coarse |

## Gotchas

- A figure that is not collidable is a bigger *picture* and nothing else: enemies shoot through the wings and hit the dot.
- Collidable parts take knockback and body damage like a body. Three big ones make a wide, slow-feeling tank.
- The same flag works on a projectile's parts: a thrown web catches shapes only where its collidable hooks are (lesson 13).
