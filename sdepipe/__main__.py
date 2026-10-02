import argparse, json, os, sys, urllib.request, zipfile, io

from .build import build, apply_patches, dump
from .validate import validate

LATEST = "https://developers.eveonline.com/static-data/tranquility/latest.jsonl"
ZIP = "https://developers.eveonline.com/static-data/tranquility/eve-online-static-data-{build}-jsonl.zip"
NEEDED = ("_sde", "categories", "groups", "types", "typeDogma", "dogmaAttributes", "dogmaEffects",
          "dbuffCollections", "dynamicItemAttributes", "fighterAbilities", "fighterAbilitiesByType",
          "marketGroups", "metaGroups", "dogmaUnits", "typeBonus", "cloneGrades", "mapRegions", "mapConstellations",
          "mapSolarSystems", "mapSecondarySuns", "systemWideEffects", "typeLists")


def latest_build() -> int:
    with urllib.request.urlopen(LATEST, timeout=60) as r:
        for line in r.read().decode().splitlines():
            obj = json.loads(line)
            if obj.get("_key") == "sde":
                return int(obj["buildNumber"])
    raise SystemExit("no sde record in latest.jsonl")


def download(build_no: int, dest: str) -> None:
    os.makedirs(dest, exist_ok=True)
    url = ZIP.format(build=build_no)
    print(f"downloading {url}", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=600) as r:
        data = r.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for n in zf.namelist():
            base = os.path.basename(n)
            if base.endswith(".jsonl") and base[:-6] in NEEDED:
                with open(os.path.join(dest, base), "wb") as fh:
                    fh.write(zf.read(n))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sdepipe")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("latest", help="print latest TQ SDE build number")
    d = sub.add_parser("download"); d.add_argument("--build", default="latest"); d.add_argument("--dest", required=True)
    b = sub.add_parser("build"); b.add_argument("--sde", required=True); b.add_argument("--out", required=True)
    b.add_argument("--patches", default=os.path.join(os.path.dirname(__file__), "..", "patches"))
    args = ap.parse_args(argv)
    if args.cmd == "latest":
        print(latest_build())
    elif args.cmd == "download":
        bn = latest_build() if args.build == "latest" else int(args.build)
        download(bn, args.dest)
        print(bn)
    elif args.cmd == "build":
        ds = build(args.sde)
        apply_patches(ds, args.patches)
        errs = validate(ds)
        for e in errs[:50]:
            print("VALIDATION:", e, file=sys.stderr)
        manifest = dump(ds, args.out)
        print(json.dumps(manifest, indent=2))
        if errs:
            sys.exit(1)


if __name__ == "__main__":
    main()
