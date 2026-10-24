# Verification code — review of Rick's Theorem I / Theorem I_OG (2026-10-24 c2)

Target: `proofs/2026-10-24-integer-window-and-OG-twin.md` in `grandpa-rick/rick-research`,
reviewed at commit `7ff2361d182d258dbf6c829c4aa97bcfd9fffc8a` (the file's last-touched
commit; `origin/main` had moved to `b44a146` by review time, but not this file).

Engines are mine, not Rick's:
- `demazure.py`  — type C_m (Sp_{2m}) Demazure characters → H_kappa(j) on LG(m,2m). From 10-23.
- `demazureB.py` — type B_m (SO_{2m+1}) Demazure characters → H^OG_kappa(j) on OG(m,2m+1). NEW
  this session; this is the OG positive control my 10-24 census did not have.
- `fast.py`      — O(1) p=1 KLG coefficient closed form, on the shape R(theta).
- `q30thm.py`    — Rick's new Theorem Q30 intrinsic criterion vs brute-force KLG enumeration.

Scripts:
| file | what it checks | result |
|---|---|---|
| `direct.py`  | direct negative-weight Demazure eval vs interpolated Hilbert polynomial | 0/522 mismatches (answers Rick's Q33) |
| `window.py`  | Theorem I + I_OG zero window, vanishing/strictness/monotonicity, m<=6 | 0 failures; `negctl()` = window shifted +-1 |
| `lemmas.py`  | Lemma 0, Lemma A (i)-(v), Lemma Ch', 2 negative controls, m<=8 | A(iii) 502/502; see F1 for the one scope slip |
| `q30thm.py`  | Theorem Q30 closed form, with a wrong-shape control | 3025/3025; control fires 528/3025 |
| `lemmaA3.py` | the shorter proof of Lemma A(iii) offered in the review | 502/502 and 293/293 |
| `thmB.py`    | Theorem B conclusion (owed from UID 841) + `a>=m` control | 150/150; control fires |
| `rinv.py`    | is the p=1 KLG count R-invariant? | NO — 528/3024 pairs disagree |

`.out` files are the captured runs.

Caveat carried from the brief: `comb.py` and `testZ.py` (copied from `code-1023-rickZ/`) run a
module-level test suite off `sys.argv[1]` on import. `fast.py` and `q30thm.py` are self-contained
to avoid that.

## Added after the first commit: referee of Rick's §3.3 (his UID 850 ask)

UID 850: *"Two steps are hand-written and I have re-read them only once: §3.3 (BR Cor 5.6 at
p=1, by induction against Thm 5.5) and §9.3 … Please referee those two."* §3.3 is what my
Finding 2 leans on, so it is refereed here.

| file | what | result |
|---|---|---|
| `referee33.py` | implements BR Thm 5.5's recursion `C(theta,p)` **from the statement** (north-east arm, theta-hat, cases (i)-(iv)) and compares `C(phi,1)` against brute-force KLG enumeration | **1243/1243** shifted skew shapes, `nu_1 <= 6` |
| `referee33_controls.py` | five negative controls, each lesioning a coefficient that is **live at p=1** | all five **FIRE** |
| `cases.out` | which Thm 5.5 cases the shape set exercises | (i) 36, (ii) 55, (iii) 148, (iv) 180, non-rim 824 |

**My first control was silent and the control was wrong, not the test.** It lesioned the
coefficient of `C(theta-hat, p-a)` in case (iv) a=1 — which at p=1 is `C(theta-hat, 0) = 0`,
identically zero because theta-hat is non-empty. A lesion on a dead term cannot show. Re-aimed
at the live coefficients, all five arms fire (40, 74, 62, 43, 43 of 1243). `referee33_controls.py`
keeps the dead-term lesion at the bottom, labelled, so the distinction stays on the record.

At p=1 the live arms of Thm 5.5 reduce to exactly: (iii) a=1 -> `-C(hat,1)`; (iv) a=1 ->
`-2C(hat,1)`; (iv) a=2 -> `+C(hat,1)`; a>=3 -> 0; plus the (i)/(ii) row/column base cases. That
is precisely the case list §3.3 walks through, so his decomposition is the right one.
