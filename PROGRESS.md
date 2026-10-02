# PROGRESS (eve-sde-pipeline)

## Done
- `sdepipe latest|download|build`, deterministic gzip JSON dataset v1, invariants validator, unit tests.
- GitHub Actions workflow (`.github/workflows/sde.yml`): every 6 h, release `sde-<build>` if new.
- Built locally for TQ build 3569502: 10 745 types, 3 422 effects, 2 871 attrs, 276 dbuffs, 417 mutaplasmids;
  7.27 MB JSON / 0.70 MB gz; ~2.7 s.

## Next
- CHANGELOG diff between builds; `changes/<build>.jsonl` use.
- Patches for Pyfa custom effects (system beacons), damage/target profile presets, implant-set metadata,
  jargon/search aliases, old-name conversions.
- Optional binary snapshot (postcard) for faster engine load.
