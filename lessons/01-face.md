---
title: A face that keeps the team colour
summary: Paint anything you like over the body, as long as the body itself stays on Team color and shows through somewhere.
pack: lesson-01-face
tank: Face
---

## What you see

A yellow face with eyes, a smile and blue cheeks. Enemies see the same face with red cheeks. That is the whole point: in team modes players must be able to tell whose tank is whose, and the rule we hold every tank to is **a team-coloured area on every tank, and every damaging shot in the team colour**.

## The trick

!chalk(01-face)

The body is the only thing the game colours for you. Leave it on **Team color**, then cover it with a part of exactly the same size placed **over** the body, and draw the face on top of that. Anything you set to **Same color as the body** then follows the team too: the cheeks here, a collar, a hat band, the lining of a cape.

Since the editor update of October 2026 there is a second way: paint the body with a **Custom color** (a hex code) instead of a palette swatch. A body coloured that way still gives its Same-color parts the **team** colour, so the cover is not needed (lesson 21). The cover is still the trick for a body in a palette colour.

```scene
{"steps": [
 {"show": [], "focus": "Tank body", "say": "Keep the body on **Team color**. It is the hitbox, and the only thing the game recolours per team."},
 {"show": ["face cover"], "say": "A circle part of **Size 50** at **Offset 0, 0**, placed **over** the body, covers it exactly. Yellow here."},
 {"show": ["face cover", "eye left", "eye right"], "say": "Eyes: two White circles of **Size 10** at **Offset X 14, Offset Y ±17**, over the body."},
 {"show": ["face cover", "eye left", "eye right", "pupil left", "pupil right"], "say": "Pupils: Charcoal circles of **Size 4**. Anything this small shows only its outline, which is fine for a pupil."},
 {"show": ["face cover", "eye left", "eye right", "pupil left", "pupil right", "smile 1", "smile 2", "smile 3", "smile 4"], "focus": "smile 2", "say": "The smile is four short hair-thin barrels over the body (**Fires: Nothing**, **Width at base 0.12×**). A curve is always a chain of short straight pieces; lesson 02 has the details."},
 {"show": ["face cover", "eye left", "eye right", "pupil left", "pupil right", "smile 1", "smile 2", "smile 3", "smile 4", "cheek left (team)", "cheek right (team)"], "focus": "cheek left (team)", "say": "Cheeks set to **Same color as the body** take the team colour, so the team still shows through the face."},
 {"live": true, "say": "**Play.** The shots stay team-coloured too: a projectile with no colour of its own uses the team colour."}
]}
```

## Numbers that matter

| Thing | Value | Why |
|---|---|---|
| Cover part | **Size** = Body size, over the body | A round body is drawn at its Body size; a polygon body at 1.3 × that, so a polygon cover needs Size × 1.3 |
| Team accents | **Same color as the body** | They take the hull's colour, which is the team colour only while the hull is on Team color |
| Shots | leave the projectile's colour unset | Team colour for free |

## Gotchas

- The cover must be **over** the body (above the Tank body row). Under it, the body paints over it and you see plain blue.
- If you give the body a **palette** colour of its own, nothing follows the team any more, including Same-color parts. Cover it instead, or use a Custom (hex) colour, which keeps the Same-color parts on the team (lesson 21).
- A figure that must be a fixed colour (a black cat, a white ghost) still needs a team spot somewhere: a collar, the eyes, a bubble.

## Where we used it

::: seen
![Trick-or-Treater: a team hull under a face cover, team showing in the bag](img/halloween-trick-or-treater.png)
![Babayaga: green face, team colour on the hat band and wand star](img/halloween-babayaga.png)
![Vlad: crimson cape with a team lining](img/halloween-vlad.png)
:::
