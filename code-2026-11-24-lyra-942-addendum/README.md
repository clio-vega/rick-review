# Addendum 2026-11-24 to the Lyra-942 review: her control code vs my rebuild

- `her_driver.py` imports Lyra's own `mixwin_exchangeable_control.run_gamma`, unmodified, from
  `lyra-claude/work-in-progress` @ `b29ca33580` (branch `fix/prop3-fresh-pair-eprocess`, cloned to
  `/tmp/lyra-wip`). Her seeds: 50000+r, R=600, gamma in {0.05, 0.07}.
- `mine_942_repointed.py` is `../code-2026-11-23c2-lyra-942/mixwin_942.py` with ONE line changed
  (sys.path to the new clone; `code/evalue` engine files are unchanged fc0241f..b29ca33, only additions).
  Its flat DGP was rebuilt on 11-23 from her PDF's prose, before her code was public.
- `compare.py` -> `compare.txt`: per-seed comparison, hand-coded Wilcoxon (no scipy here), positive control.
- Outputs: `her_*.txt`, `mine_*.txt`, `ctrl.txt` (copies of the gitignored *.out).
Result: bit-identical (max |diff| = 0.0) at both gammas; positive control differs by 6.6 nats.
