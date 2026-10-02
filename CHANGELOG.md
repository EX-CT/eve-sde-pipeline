# CHANGELOG

Dataset `format_version` stays **1**: all changes below only add data, and the eve-dogma-rs loader ignores keys it
doesn't know. `dataset_revision` counts content revisions of the pipeline output. For revision > 1, files and
tags carry a suffix (`dataset-<build>-r<rev>.json.gz`, release `sde-<build>-r<rev>`), so published files are never
overwritten.

## Revision 3 (pipeline 0.3.0, 2026-10-03)
- `environment.effect_beacons[*].dbuffs`: the warfare buffs `{buffID: value}` that each environment beacon emits
  (abyssal weather, clouds, …). Engines can apply them the way they apply fleet command bursts.
- Proposed patches (`patches/proposed/`, opt-in with `--with-proposed`, not in releases) for the Pyfa effects
  that have no modifierInfo.
- `sdepipe diff` (Markdown + JSON, with an optional CCP `changes/<build>.jsonl` summary), and `sdepipe names`.
- CI: releases `sde-<build>-r<rev>` with CHANGELOG-<build>.md, diff JSON, Pyfa coverage report, manifest.
- Verified: with r1 and r3, engine A (eve-dogma-rs) and variant K give identical output on all 297 bench cases.

## Revision 2 (pipeline 0.2.0, 2026-10-03; local only, never released)
- New top-level sections:
  - `market_groups`, `meta_groups`, `units`
  - `traits` (ship bonus text: role/misc/per-skill, en + zh)
  - `required_skills`, `clone_grades`
  - `environment` (wormhole classes, systems with a WH class or effect beacon, effect beacons classified by kind,
    system-wide effects, type lists)
  - `names_i18n.zh` for groups/categories/market groups/meta groups/attributes/units
  - `dataset_revision`
- Every section that existed in r1 is byte-identical to r1.

## Revision 1 (pipeline 0.1.0)
- First dataset: types/groups/categories/attributes/effects (compressed modifierInfo), dbuffs, mutaplasmids,
  fighter abilities, zh type names. Release `sde-3569502`.
