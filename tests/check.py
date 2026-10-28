#!/usr/bin/env python3
"""Check this repository and saved outputs; does not run or grade a model.

Development tools only: Python 3.10+, PyYAML, and Pandoc.
This is not a replacement for skills-ref or a universal Markdown validator.
"""

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    sys.exit("Missing development tool: install PyYAML to run these checks.")

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def check(condition, message):
    if not condition:
        ERRORS.append(message)


def walk(value):
    if isinstance(value, dict):
        if "t" in value:
            yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def markdown(text, label, base=None):
    # Pandoc also accepts malformed fences as text; check closure separately.
    fence = None
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if not match:
            continue
        marks, tail = match.groups()
        if fence is None:
            fence = marks
        elif marks[0] == fence[0] and len(marks) >= len(fence) and not tail.strip():
            fence = None
    check(fence is None, f"{label}: unclosed code fence")
    proc = subprocess.run(
        ["pandoc", "--from=gfm+tex_math_dollars", "--to=json"],
        input=text, text=True, capture_output=True, check=False,
    )
    check(proc.returncode == 0, f"{label}: Pandoc parse failed: {proc.stderr}")
    if proc.returncode:
        return []
    nodes = list(walk(json.loads(proc.stdout)))
    anchors = {node["c"][1][0] for node in nodes if node["t"] == "Header"}
    previous = 0
    for node in nodes:
        if node["t"] == "Header":
            level = node["c"][0]
            check(level <= previous + 1, f"{label}: heading jumps to level {level}")
            previous = level
        if base is not None and node["t"] in {"Link", "Image"}:
            target = node["c"][-1][0]
            url = urlsplit(target)
            if not url.scheme and not url.netloc and not url.path and url.fragment:
                check(unquote(url.fragment) in anchors,
                      f"{label}: missing heading target {target}")
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            check(not path.startswith("/"), f"{label}: nonportable absolute link {path}")
            check((base / path).exists(), f"{label}: missing local target {path}")
    return nodes


def main():
    if not shutil.which("pandoc"):
        sys.exit("Missing development tool: install Pandoc to run Markdown checks.")
    source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    parts = source.split("---", 2)
    check(len(parts) == 3 and not parts[0].strip(), "SKILL.md: missing frontmatter")
    if len(parts) != 3:
        return
    meta = yaml.safe_load(parts[1])
    check(isinstance(meta, dict), "SKILL.md: metadata must be a mapping")
    if not isinstance(meta, dict):
        return
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    check(set(meta) <= allowed, "SKILL.md: unknown frontmatter field")
    name = meta.get("name", "")
    check(isinstance(name, str) and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name))
          and len(name) <= 64, "SKILL.md: invalid name")
    check(name == ROOT.name, "SKILL.md: name must match directory")
    desc = meta.get("description", "")
    check(isinstance(desc, str) and 1 <= len(desc) <= 1024, "SKILL.md: invalid description")
    check(len(parts[2].splitlines()) < 500, "SKILL.md: exceeds recommended 500 lines")
    if "compatibility" in meta:
        value = meta["compatibility"]
        check(isinstance(value, str) and 1 <= len(value) <= 500, "Invalid compatibility")
    if "metadata" in meta:
        value = meta["metadata"]
        check(isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, str)
              for k, v in value.items()), "Invalid metadata string map")

    cases = json.loads((ROOT / "tests/cases.json").read_text())["evals"]
    ids = [c["id"] for c in cases]
    check(len(ids) == len(set(ids)), "Duplicate evaluation IDs")
    for case in cases:
        check(bool(case["prompt"] and case["assertions"]), f"Case {case['id']}: incomplete")
        for file in case["files"]:
            check((ROOT / file).is_file(), f"Case {case['id']}: missing fixture {file}")
    triggers = json.loads((ROOT / "tests/trigger-cases.json").read_text())["cases"]
    check(len({t["id"] for t in triggers}) == len(triggers), "Duplicate trigger IDs")
    check(all(type(t["should_trigger"]) is bool for t in triggers), "Invalid trigger labels")

    docs = [p for p in ROOT.rglob("*.md") if "fixtures" not in p.parts]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            text = parts[2]
        markdown(text, str(path.relative_to(ROOT)), path.parent)

    # Saved outputs are evidence, not freshly generated model trials.
    result_file = ROOT / "tests/results.json"
    outputs = []
    if result_file.exists():
        results = json.loads(result_file.read_text())
        if hashlib.sha256(source.encode()).hexdigest() != results["final_skill_sha256"]:
            print("NOTE: saved model trials used an earlier SKILL.md; checking their "
                  "integrity does not validate the current skill's behavior.")
        for file, digest in results["published_fixture_sha256"].items():
            path = ROOT / file
            check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                  f"Published fixture changed: {file}")
        for artifact in results["artifact_manifest"]:
            if artifact.get("public_example"):
                path = ROOT / artifact["public_example"]
                check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()
                      == artifact["sha256"], f"Example changed: {path.name}")
        outputs = results["runs"]
        check(len({(r['iteration'], r['variant'], r['case_id']) for r in outputs})
              == len(outputs), "Duplicate saved run IDs")
        for run in outputs:
            label = f"saved/{run['iteration']}/{run['variant']}/{run['case_id']}"
            check(hashlib.sha256(run["output"].encode()).hexdigest() == run["sha256"],
                  f"{label}: saved response checksum mismatch")
            nodes = markdown(run["output"], label)
            if run["case_id"] == "12":
                code = [n["c"][1] for n in nodes if n["t"] == "CodeBlock"]
                check(any('ready || retry' in s and 'puts("a|b & <ok>");' in s for s in code),
                      f"{label}: C operators/text changed by Markdown parsing")
                check(any('```c' in s and 'int mask = a | b;' in s for s in code),
                      f"{label}: nested fence example lost")
    else:
        print("SKIP: local tests/results.json is absent; no saved model trials checked.")
    print(f"Checked metadata, {len(cases)} cases, {len(triggers)} trigger labels, "
          f"{len(docs)} Markdown files, and {len(outputs)} saved responses.")


if __name__ == "__main__":
    main()
    if ERRORS:
        print("\n".join(f"FAIL: {e}" for e in ERRORS))
        sys.exit(1)
    print("PASS: repository and saved-response checks (no model inference performed).")
