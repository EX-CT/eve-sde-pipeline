# eve-sde-pipeline

CCP's official **EVE Online SDE (JSONL)** → compact, deterministic, versioned **engine dataset** used by
[`eve-dogma-rs`](https://github.com/EX-CT/eve-dogma-rs) and [`eve-fit-mcp`](https://github.com/EX-CT/eve-fit-mcp).
Design: [eve-fit-docs/04-sde-pipeline](https://github.com/EX-CT/eve-fit-docs/blob/main/docs/04-sde-pipeline.md).

中文：从 CCP 官方 JSONL SDE 生成引擎数据包（约 0.7 MB gz），GitHub Actions 每 6 小时检查新 build 并发布 Release `sde-<build>`。

```bash
python -m sdepipe latest                      # current TQ build number
python -m sdepipe download --dest sde         # fetch & extract the needed JSONL files
python -m sdepipe build --sde sde --out dist  # -> dist/dataset-<build>.json.gz + manifest.json
SDEPIPE_DIST=dist python -m unittest discover -s tests
```

Pure Python stdlib, no dependencies. Output is byte-for-byte deterministic (sorted keys, gzip mtime 0).

* Kept categories: Ship, Module, Charge, Skill, Drone, Implant, Subsystem, Structure, Structure Module, Fighter,
  mutaplasmid-related types, and Celestial types that carry dogma effects (system/wormhole/abyssal beacons).
* `modifierInfo` compressed to tuples `[func, domain, modifiedAttr, modifyingAttr, op, groupOrSkill]`
  (codes in `sdepipe/build.py`).
* `patches/*.json` are applied after conversion (`{"id":…, "description":…, "set": {"types": {"587": {...}}}}`).

Licence: code MIT. EVE data © CCP hf., used under CCP's third-party developer licence (see `LICENSE.EVE`).
