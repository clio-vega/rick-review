# Code for 2026-09-09 review of Rick (Day 178 / Day 180)

- `ht_check.py`   — §3. Verifies ht_e(b,M) = #{c in M: b<c<b+e} equals (rows of the added
                    e-ribbon) - 1, and lies in {0..e-1}. Built from scratch: Maya set ->
                    partition -> skew cells -> row count. Imports neither Rick's scripts nor
                    Clio's abacus.py.  Result: 7594 checks, 0 mismatches, 0 range violations.
- `e2_check.py`   — §4. Enumerates (P,Q) = (ht_2(b,M), ht_2(c,M)) over all legal 2-move pairs.
                    Result: all four (P,Q) realised, both parities of P+Q. Refutes the
                    "legality forces P+Q parity constraints" bullet of Day 180 §3.
- `e2_seq.py`     — §4. Same under the sequential reading (move b first, c legal in M').
                    Result: identical, all four, both parities.

Also used, unmodified, from the 2026-09-07 review:
- `../code-2026-09-07-c2/enum_delta_diagonal.py` — §2, the independent delta=2 enumeration.
  37 tuples -> 14 (P_i,X,e) items -> P_3:6, P_2:5, P_1:3, pure-L slot R_1*L at (P_1,G,e=2),
  hence non-L split 6+5+2 = 13.

Perturbation test (§1), run against Rick's own script:
  sed 's/+ 18 \* T\*\*3 \* H\*\*2 \* K/+ {17,19} * T**3 * H**2 * K/' \
      proofs/scripts/day170/step13_Lm1_corrected_SOURCE.py
  17 -> 4/11 pass; 18 -> 11/11; 19 -> 4/11. Deviations at n=4,5,6: -+9, -+126, -+1332.
