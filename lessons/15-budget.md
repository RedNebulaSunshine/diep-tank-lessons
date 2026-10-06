---
title: Staying under the lobby's budget
summary: The lobby refuses a tank that fires too much, keeps too much alive or has too many pieces; here is what counts and the one stat that buys you room.
---

## What you see

Every moving trick in these lessons is a barrel that fires: pistons, bite points, trail droppers, dashes. The game counts all of them, at once, with every button held and the Reload stat maxed, and refuses the pack if the total is over the line. The editor shows the same check before you load: a tank over the line carries an **Over budget** tag, and the pack screen says why.

## The six limits

| Limit | The message | What counts |
|---|---|---|
| 120 a second | *fires too much: R/120 per second, A/250 in the air* | Everything created per second: every barrel on the body, left click, right click and Always fire together, at the tank's Reload cap |
| 250 in the air | (same message) | Of those, how many are alive at once: per second × Lifetime (an unset Lifetime counts as 3 s) |
| 2000 of room | *takes too much room: N/2000 bullet-areas in the air* | The area of everything alive, a standard bullet being 1; size counts squared, so a 2× shot costs 4 and a 3× shot 9 |
| 64 per volley | *puts N entities out per volley; a tank may put out 64* | One pull of every trigger |
| 96 pieces | *has N pieces; a tank may have 96* | Parts, barrels and turrets on the body **plus** everything every projectile carries |
| 96 drones | *has N drones; a tank may have 96* | Max drones of every drone barrel |

## How a shot is counted

!chalk(15-budget)

- A barrel fires every ⌈15 × 0.914^cap × Reload⌉ ticks at 25 ticks a second, where *cap* is the tank's Reload stat cap. At cap 7 a Reload-1 barrel is about 3 shots a second, at cap 12 about 4, and short reloads cost more than proportionally (Reload 0.25 at cap 12 is 12.5 a second).
- Each shot counts **1 plus everything its projectile carries**: parts, drawn rods, barrels, turrets. A web of 24 rods is 25 per shot. A drawn companion is as expensive as the hull's art.
- A barrel riding a projectile adds its own shots once per live copy, if it fires: always on a drone; on a bullet only with Always fire or when it sits on one of the projectile's turrets. **Fires when it bursts** counts once per shot.
- Drones do not count per second; they count against the 96 and against room.

## The one stat that buys room

The **Stat points** row at the bottom of the tank's panel sets the max level of each stat. Set **Reload** to **0** and every barrel fires at its slowest, so the whole tank costs a fraction of the budget. A player-built character pack does this on 47 of its 60 playable classes, and it is how our tanks fit a dozen moving parts under the line. Players lose the Reload upgrade, which for a figure that fights with jaws and limbs is no loss.

## Reading the numbers before you import

The editor's pack screen shows a size bar and tags the tanks the lobby would refuse: filter the list by **Over budget**, and the tank's row says *fires too much* or *takes too much room*. If you build packs with the [diep-pack skill](https://github.com/RedNebulaSunshine/diep-pack-skill), its validator prints all six figures for every tank before you ever open the editor, and these lesson tanks were checked that way.

## Rules of thumb

- Specks for pistons at Reload 0.5 cost about 8 a second each at cap 12. Four pumping legs plus a trail is already most of the budget without a Reload cap of 0.
- Short **Lifetime** on anything cosmetic: 0.1 s for specks and dashes, 0.2 s for bite points.
- Keep decorated projectiles small in pieces, and never fire them from a barrel that also rides a projectile.
- There is no margin to leave: the biggest player-built tanks sit at 119.9 a second and exactly 96 pieces.
