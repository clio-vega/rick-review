"""Two-arm positive control for registry_validate.py's agent-summary boundary rule.
Clio 2026-10-22. A silent all-clear with no positive control is the fault class
that has cost me most this month, so: plant a node that MUST trip the rule, in
both the bare-id and the locator-decorated spelling, and confirm it fires.
"""
import json, subprocess, sys, tempfile, os
ROOT = "/home/clio/projects"
SRC  = json.load(open(f"{ROOT}/memory/reading/sources.json"))["sources"]

# 2312.17200 (Mihalcea-Naruse-Su) is held at 'agent-summary' in my own index.
BAIT = "2312.17200"
assert SRC[BAIT]["extraction"] == "agent-summary", SRC[BAIT]

def run(reg, extra=()):
    p = subprocess.run([sys.executable, f"{ROOT}/code/registry_validate.py", reg,
                        "--sources", f"{ROOT}/memory/reading/sources.json", *extra],
                       capture_output=True, text=True, cwd=ROOT)
    return p.stdout + p.stderr

def plant(sources, trust="proved"):
    tree = {"id": "root", "approach": "control", "trust": trust, "children": [],
            "sources": sources}
    return {"status": trust, "tree": tree}

def probe(label, sources, trust="proved", expect_fire=True):
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(f"{d}/proofs/registry", exist_ok=True)
        f = f"{d}/proofs/registry/control.json"
        json.dump(plant(sources, trust), open(f, "w"))
        out = run(f, ("--proofs-dir", "skip"))
    fired = "every cited source is" in out
    ok = (fired == expect_fire)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:52s} rule fired={fired} (expected {expect_fire})")
    return ok

print("== Arm 1: the rule must FIRE on an agent-summary-only 'proved' node ==")
a = probe("bare id, proved                       (must fire)", [BAIT], "proved", True)
b = probe("locator-decorated id, proved          (must fire)",
          [f"arXiv:{BAIT} Thm 5.5 L1234-1240"], "proved", True)
c = probe("legacy-style id spelling, proved      (must fire)",
          ["arXiv:2312.17200v2 §5.5"], "proved", True)

print("\n== Arm 2: the rule must NOT fire when it should not ==")
d = probe("same source but trust='computed'      (must NOT fire)", [BAIT], "computed", False)
e = probe("a verified-quote source, proved       (must NOT fire)", ["1112.5223"], "proved", False)
f = probe("mixed: agent-summary + verified-quote (must NOT fire)",
          [BAIT, "arXiv:1112.5223 §8.3 L3354"], "proved", False)

print("\n== Arm 3: the locator spelling must now RESOLVE (no 'not in index' warning) ==")
with tempfile.TemporaryDirectory() as dd:
    os.makedirs(f"{dd}/proofs/registry", exist_ok=True)
    fn = f"{dd}/proofs/registry/control.json"
    json.dump(plant(["arXiv:2610.15344 eq:allcard-Bhat-product-C L4668"], "computed"), open(fn,"w"))
    out = run(fn, ("--proofs-dir", "skip"))
g = "not in the sources index" not in out
print(f"  [{'PASS' if g else 'FAIL'}] decorated '2610.15344' resolves to the index entry")

print("\nALL CONTROL ARMS PASS:", all([a,b,c,d,e,f,g]))
