"""Inspect an npm tarball and create a verified portable runtime ZIP."""
from pathlib import Path, PurePosixPath
from hashlib import sha256
import argparse
import json
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def digest(data):
    return sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tarball", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(exist_ok=False)
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    inventory = json.loads((ROOT / "catalog/files.json").read_text(encoding="utf-8"))
    expected = {x["path"] for x in inventory} | {"catalog/files.json"}
    archive = {}
    with tarfile.open(args.tarball, "r:gz") as saved:
        for member in saved:
            path = PurePosixPath(member.name)
            assert not path.is_absolute() and ".." not in path.parts and "\\" not in member.name
            assert path.parts[0] == "package" and not member.issym() and not member.islnk()
            if member.isdir():
                continue
            assert member.isfile()
            rel = "/".join(path.parts[1:])
            assert rel not in archive
            archive[rel] = saved.extractfile(member).read()
    assert set(archive) == expected, sorted(set(archive) ^ expected)
    for rel, data in archive.items():
        assert data == (ROOT / rel).read_bytes(), rel
        assert not any(part in {".private-archive", "dev", "tests", "build", ".test-deps", ".npm-cache", "__pycache__"} for part in PurePosixPath(rel).parts), rel
    for entry in inventory:
        assert digest(archive[entry["path"]]) == entry["sha256"], entry["path"]
    mapping = json.loads(archive["docs/humanizer-source-map.json"])
    mapped = {item["destination"] for item in mapping}
    for name in ("humanizer-main", "academic-humanizer-main"):
        assert f"resources/upstream/{name}/LICENSE" in mapped
    for item in mapping:
        assert digest(archive[item["destination"]]) == item["sha256"], item["destination"]
    target = out / args.tarball.name
    target.write_bytes(args.tarball.read_bytes())
    plugin_zip = out / ("academic-research-assistant-" + version + ".zip")
    with zipfile.ZipFile(plugin_zip, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as saved:
        for rel, data in sorted(archive.items()):
            info = zipfile.ZipInfo("academic-research-assistant/" + rel, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            saved.writestr(info, data, compresslevel=9)
    with zipfile.ZipFile(plugin_zip) as saved:
        assert saved.testzip() is None
        for rel, data in archive.items():
            assert saved.read("academic-research-assistant/" + rel) == data
    sums = {p.name: digest(p.read_bytes()) for p in [target, plugin_zip]}
    (out / "SHA256SUMS.txt").write_text("".join(h + "  " + name + "\n" for name, h in sums.items()), encoding="utf-8")
    report = {"passed": True, "version": version, "runtime_files": len(archive),
              "skills": sum(p.startswith("skills/") and p.endswith("/SKILL.md") for p in archive),
              "all_archive_bytes_match_source": True, "excluded_private_and_developer_files": True,
              "sha256": sums, "publication": "Local artifacts only"}
    (out / "package-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
