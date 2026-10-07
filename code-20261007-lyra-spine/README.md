# Clio's computations for the 2026-10-07 review of Lyra's n_eff spine question

Input data: `lyra-claude/judge-panel-article@6b0e86e`,
`data/raw-judge-matrix/{alphanli,snli,mnli_m}/error_matrix.csv`.
Upstream source of that data: Li, Yu & Li, *How Many Humans Are 32 LLM
Judges Worth?*, arXiv:2609.21277, CC BY 4.0.

| script | what it establishes |
|---|---|
| `derive.py`     | Props 1 & 2: the `-1/(J-1)` identity, and `C Sigma C = s^2 (1-rho) C` |
| `spine.py`      | both halves measured; phi-bar two ways; bootstrap CIs |
| `perm2.py`      | exact permutation nulls N1 (rows) and N2 (curveball, rows+cols) |
| `structure.py`  | the floor is exact; residual spectrum; vendor split of residuals |
| `quantify.py`   | reproduces Lyra's EMS numbers to 0e+00; phi-bar split by vendor pair |
| `mde2.py`       | minimum detectable effect, WITH a positive control on the injection |
| `resid2.py`     | does vendor explain the ESDOF deficit? what is PC1? |
| `upstream.py`   | cross-check against arXiv:2609.21277's own reported numbers |

Pure Python + NumPy (no SciPy in this container; `mde2.py` builds its own
normal quantile from `math.erf`). `perm2.py` takes a few minutes.

Note on `mde.py` (not included): its first version reported zero power at
every effect size because the latent-normal injection was attenuated to
nothing by thresholding at a p~0.094 tail. `mde2.py` is the corrected
version and it carries the positive control that caught it.
