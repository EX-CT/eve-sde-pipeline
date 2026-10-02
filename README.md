# eve-sde-pipeline

CCP's official **EVE Online SDE (JSONL)** → compact, deterministic, versioned **engine dataset** used by
[`eve-dogma-rs`](https://github.com/EX-CT/eve-dogma-rs) and [`eve-fit-mcp`](https://github.com/EX-CT/eve-fit-mcp).
Design: [eve-fit-docs/04-sde-pipeline](https://github.com/EX-CT/eve-fit-docs/blob/main/docs/04-sde-pipeline.md).

中文：从 CCP 官方 JSONL SDE 生成引擎数据包（约 0.7 MB gz），GitHub Actions 每 6 小时检查新 build，构建、校验、测试，生成与上一版的差异报告和 Pyfa 效果覆盖报告，并发布 Release `sde-<build>-r<revision>`。

```bash
python -m sdepipe latest                      # current TQ build number
python -m sdepipe download --dest sde         # fetch & extract the needed JSONL files
python -m sdepipe build --sde sde --out dist  # -> dist/dataset-<build>-r<rev>.json.gz + manifest.json
SDEPIPE_DIST=dist python -m unittest discover -s tests
python -m sdepipe diff OLD.json.gz NEW.json.gz --md CHANGELOG.md --json diff.json [--ccp-changes changes.jsonl]
python tools/pyfa_effects.py --pyfa PYFA_DIR --dataset NEW.json.gz --engine-names tools/engine-effect-names.json --out reports
```

Pure Python stdlib, no dependencies. Output is byte-for-byte deterministic (sorted keys, gzip mtime 0).

* Kept categories: Ship, Module, Charge, Skill, Drone, Implant, Subsystem, Structure, Structure Module, Fighter,
  mutaplasmid-related types, and Celestial types that carry dogma effects (system/wormhole/abyssal beacons).
* `modifierInfo` compressed to tuples `[func, domain, modifiedAttr, modifyingAttr, op, groupOrSkill]`
  (codes in `sdepipe/build.py`).
* `patches/*.json` are applied after conversion (`{"id":…, "description":…, "set": {"types": {"587": {...}}}}`).

## Automation (`.github/workflows/sde.yml`)
Triggers: cron every 6 h, manual dispatch (`build`, `force`), and pushes to `sdepipe/`, `patches/` or `tests/`.
1. Resolve the TQ build from `latest.jsonl` and derive the tag `sde-<build>-r<rev>`. Skip if that release exists.
2. Download, build, validate, then run the unit tests (a failure stops the release).
3. Diff against the previous `sde-*` release and summarise CCP's `changes/<build>.jsonl`, giving `CHANGELOG-<build>.md`
   and `diff-<build>.json`.
4. Pyfa coverage: classify every effect handler in Pyfa master `eos/effects.py`, giving `pyfa-effects-coverage.md` and `.json`.
5. `gh release create`: dataset, `manifest.json`, `manifest-<build>.json`, changelog, diff, coverage, LICENSE.EVE.
   The changelog becomes the release notes, and the newest release is marked Latest.

Consumers get the newest release with `gh release download -R EX-CT/eve-sde-pipeline -p 'dataset-*.json.gz'`.

## Dataset contents
| section | what |
|---|---|
| `types` | published ships/modules/charges/skills/drones/fighters/implants/boosters/subsystems/structures/structure modules + mutaplasmid-related + dogma-carrying celestials; attrs, effects, group/category/market/meta, en name (`names.zh` for Chinese) |
| `groups`, `categories`, `market_groups`, `meta_groups`, `units` | hierarchy + names (zh in `names_i18n.zh`) |
| `attributes`, `effects` | dogma attributes (default, stackable, high-is-good, unit) and effects (category, duration/range/falloff attrs, compressed modifierInfo) |
| `dbuffs` | warfare buff collections (command bursts, environment buffs) |
| `mutaplasmids` | dynamic attribute ranges, input/output types |
| `fighter_abilities` | fighter ability slots |
| `required_skills` | per-type skill requirements `{skill: level}` |
| `traits` | ship/subsystem bonus text (role, misc, per skill), en + zh |
| `clone_grades` | alpha clone skill caps |
| `environment` | wormhole classes, systems → WH class / effect beacon, effect beacons (`kind`: wormhole, abyssal, triglavian, incursion, faction_warfare, metaliminal_storm, other; `dbuffs`), system-wide effects, type lists |
| `patches` | applied data patches (`patches/*.json`); `patches/proposed/` are opt-in |

See [`reports/pyfa-effects-coverage.md`](reports/pyfa-effects-coverage.md) for which Pyfa effects modifierInfo
cannot express and how each is handled.

Licence: code MIT. EVE data © CCP hf., used under CCP's third-party developer licence (see `LICENSE.EVE`).
