---
title: Your own colours
summary: Every colour box now takes any colour as a hex code, with an opacity slider. A body painted this way still gives its Same-color parts the team colour, and the new Fallen swatch is the stock bosses' grey.
pack: lesson-21-colours
tank: Tangerine
---

## What you see

An orange tank: not the palette's Orange, a deeper one the palette never had. The square badge on it is blue to you and red to enemies. The fin at the back is see-through, and two silver studs use the new **Fallen** swatch.

## The trick

!chalk(21-colours)

Before the editor update of 6 October 2026 a colour was one of 24 swatches. Now every colour picker ends with **Custom color**: an **Edit color** dialog with a **Hex** box and an **Opacity** slider. The pack file carries the colour as a string, `#rrggbb` or `#rrggbbaa` with the opacity as the last pair, anywhere a colour goes: the body, parts, barrels, turret bases, projectiles. The editor remembers your last 22 custom colours per browser; they are not part of the pack.

```scene
{"steps": [
 {"show": [], "focus": "Tank body", "say": "**Team color** off and **Body color: Custom · Hex #e67828**. The body is now this exact orange to everyone."},
 {"show": ["badge (same color as the body)"], "say": "A square of **Size 18** over the body with **Same color as the body**. On a Custom-coloured body this does **not** take the orange: in play it shows the **team colour**, blue to you and red to enemies. (The editor's preview paints it orange, which is wrong; the mock here shows what the game does.)"},
 {"show": ["badge (same color as the body)", "stud (Fallen)", "stud right (Fallen)"], "focus": "stud (Fallen)", "say": "Two circles of **Size 11** in **Fallen**, the swatch the update added: the grey of the game's Fallen Booster and Fallen Overlord."},
 {"show": "all", "focus": "fin (40 % opacity)", "say": "A White triangle of **Size 34** behind the body with **Opacity 40 %** (the file says `#ffffff66`). In play the hull and the arena shapes show through it."},
 {"live": true, "say": "**Play.** The badge stays team-coloured and the shots do too: a projectile with no colour of its own is always the team's."}
]}
```

## Numbers that matter

| Field | Value | Notes |
|---|---|---|
| Hex | `#rrggbb` | Case does not matter; the editor stores it lower-case |
| Opacity | 25 % or more | The last pair of `#rrggbbaa`; below about 25 % only the outline reads. 50 % is a clear ghost, 80 % a tint |
| Same color as the body | the team colour | On a Custom-coloured body (seen in play 2026-10-06). On a palette-coloured body it is still the body's colour (lesson 01) |
| Fallen | `#C0C0C0` | New swatch, index 17 in the file |

## Gotchas

- **Prefer the palette when a swatch is close.** Players read the stock colours (yellow food, pink crashers, grey barrels) and the swatch names are what someone can say back to you. Reach for a hex code when the subject has a colour the palette lacks and people would notice.
- **A hex body no longer needs the cover trick.** Lesson 01 covers a team-coloured body with a same-size part because a palette-coloured body turns every Same-color part that colour. A Custom-coloured body does not, so an exact-colour figure gets its team accents for free.
- **Don't trust the editor's preview on this.** It paints Same-color parts in the body's hex colour; the game paints them in the team colour. With no team assigned yet the part draws see-through with a grey outline.
- **Opacity is for the fixed colours.** Team color and Same color are indices, not hex codes, so they cannot carry an opacity. A translucent part is always a fixed colour.
- Custom arena shapes must now use a valid hex colour too; anything else becomes the editor's default yellow.
- Translucency is an effect, not a default. A ghost, glass, smoke, a shadow or water earn it; a tank that is see-through all over just looks unfinished.
