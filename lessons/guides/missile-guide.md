---
title: The guide to creating missiles
summary: A write-up supplied by Random Troller, the author of the seeking projectile technique: unguided and guided missiles, warheads, the proximity interceptor and the MJRV salvo.
slug: missile-guide
kicker: Write-up
---

> A write-up supplied by **Random Troller**, the author of the seeking projectile technique, lightly edited from the PDF he sent in. Editor field names are in **bold**.

## Basic unguided missiles

The core principle of a missile is a self-propelling bullet. In the tank editor, this translates into a rear-firing barrel placed on the bullet itself. This barrel has a few core features:

- A low **Reload**, so it fires rapidly
- A high **Recoil** (3 or more) to generate thrust. It can be lowered if you want the missile to keep its speed from the **Bullet speed** stat.
- Low or no bullet **Damage**
- Low or no **Bullet speed**
- A low bullet **Lifetime**, crucial in keeping your tank under budget
- **Always fire** (MUST HAVE)

The primary features are the reload, recoil, bullet lifetime and always fire.

## Basic guided missile

To create a guided missile, we need a targeting system for the missile. Just like the real world, you can target the missile with a laser (manual targeting), or the missile can target by itself (automatic targeting). To make a manually targeted missile, use a drone. For automatic, use an auto turret.

For the rest of this guide, all simple guided missiles are done with auto turrets.

In the tank editor, add an auto turret to the missile. Make sure the turret is layered **below** the bullet, and the barrel is layered above the turret. This way the turret is hidden.

The auto turret itself has a few core components:

- The tracking **Range**
- The **Arc**
- **Aims with cursor**

Once the turret is on the bullet and facing 0 degrees, take the thrust barrel and put it at 180 degrees relative to the turret. **DO NOT ROTATE THE TURRET 180!**

The tracking range is how far out the missile can track its target. The arc is the angle the missile can turn to hit the target.

**Note:** the arc's angle is relative to where the missile was **fired**, not to the missile itself. This means that **only a 0 arc turret can chase**, as with any other arc it is possible to escape the missile's targeting.

### Key concept: the target field

Arc and range merge together to give the missile its "target field". The larger the missile's target field, the more ground it can hit. However, the larger the field, the harder it is to hit a specific target. In general, a large arc with a low range, or a small arc with a long range, is best. With the large arc, you want the missile to be powered mainly by thrust from the recoil of the missile's engine.

This concept of the target field is especially critical for a 0 arc missile. While it can chase any target, its range must be quite small to stop it instantly tracking a target that is behind the tank.

The example tank uses a missile with an arc of 25 and a range of 2000.

## Explosive guided missiles

The key idea behind a missile's explosion is to trigger it in one of two ways: **burst** or **right click**. In both cases, the payload is delivered by extra barrels placed on the bullet.

### Payload options

For burst-triggered explosions, only traps and bullets are viable. For right-click-triggered explosions, drones are viable as well, provided the missile stays alive.

There are two main ways to deliver the payload: one spread-focused barrel, or several accurate barrels.

- A **spread-focused barrel** has two key characteristics: a high **Spread** and many **Bullets per shot**.
- A **multiple-barrel payload** has lower spread, but several barrels are placed on the bullet. (You can also make the barrels invisible and put them anywhere on the bullet. If you want, you can even spin the bullet for more randomness.) Several barrels also let you have a full 360° explosion, whereas the single barrel fires in front of the missile.

In both cases, make the barrels very short, so they don't clip through and fire behind the target the missile strikes.

In general, a single barrel with high spread is very efficient in entities, but not accurate. A multiple-barrel payload is more consistent, but expensive in entities.

In an ideal world, the payload would be attached directly to the turret. That is bugged at the time of writing, so attach the payload to the bullet instead.

### Triggering the payload

Once you have chosen your payload, you need to decide its trigger.

- To trigger the payload with **right click**, select your payload barrels and set them to fire on right click instead (**Fires on right click**).
- To trigger the payload with **burst**, you have three options: right click, getting destroyed, and running out of time. Tick the ones you want under **Burst**, then select the payload barrels and set them to **Fires when it bursts**.

The barrels carrying the payload have three key attributes: **Launch speed**, **Bullet speed** and bullet **Lifetime**. The first two set how fast the explosion expands; the last one sets how far it expands. In most cases you want a higher bullet speed and launch speed with a minimal lifetime. That also helps keep the missile under budget.

The example is a single-barrel, randomised payload.

## Proximity interceptor missile

For a proximity interceptor, the missile not only has to track the target, it must also explode **by itself** near or on the target. That may sound difficult, but the solution is quite literally another auto turret. This kind of missile has two turrets: one for thrust and targeting, and one to control the payload.

To control the payload's trigger, you need to know these key components:

- The turret **Arc**
- The turret **Range**
- The payload's **Reload**

The first two control the payload's target field. The last one is especially important, as it stops the payload firing several times during the missile's life. Until an update lets barrels trigger a burst on the bullet they sit on, this is the way to limit how often the payload fires.

**Important:** the turret arc for interceptors cannot be too wide, or the firing mechanism will not work properly.

Done correctly, the missile triggers its payload by itself when it is near the target.

## Multiple Jointly Targeted Reentry Vehicle (MJRV)

Not as well known as the Multiple Independently targetable Reentry Vehicle (MIRV). The main limit here is the entities-per-volley limit, so every effort to cut the entities used is needed to make the MJRV possible.

The key thing about the MJRV is that the missile doesn't "split" into more missiles: all the missiles are fired at the same time. Also important: the MJRV works with **drones**, not bullets.

To make an MJRV, first create the missiles. They are based on drones, and they have two main components: the payload and the splitter.

- The **payload** is the standard burst-triggered explosion: a single, spread-based barrel.
- The **splitter** is what makes the MJRV work. In the example there are two missiles, one with a 90 degree splitter and the other with a −90 degree splitter. The key components of the splitter are a maxed-out (or very high) **Recoil** and a maxed-out (or very high) **Spread**. That lets the missiles split up properly in mid-air.

The barrel firing the missiles (the one on the tank) must have **0 Spread** and **0 Knockback**. Otherwise the missiles spread out before the splitters act. In the example, four of each missile are fired.

### Firing several drones at once

**Important!** The editor does not actually let you fire four drones at the same time. But you can trick it into letting a single drone barrel fire several at once, and control the spread and recoil of drones too. Step by step:

1. Create the missile. Make it a drone, and add the payload and splitter as usual.
2. Change the missile from a drone to a bullet type.
3. Go to the barrel that fires the missile. Now that it is a "bullet", recoil and spread can be adjusted.
4. Set the number of missiles you want to fire (**Bullets per shot**), and set **Spread** and **Knockback** to 0.
5. Go back to the missile and change its type back to drone. Now when you fire, the drone keeps the settings it had as a bullet: the spread, the recoil and the number per shot.

Once that is done and the splitter is set up, set up the firing mechanism for the missile and the MJRV is complete. Because it is drone-based, you need to **hold down left click** for the MJRV to work.
