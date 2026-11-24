"""Run Lyra's OWN run_gamma (mixwin_exchangeable_control.py @ b29ca33) unmodified, save per-seed arrays."""
import sys, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import mixwin_exchangeable_control as m
g, out = float(sys.argv[1]), sys.argv[2]
D = m.run_gamma(g, m.R)
np.savez(out, **D)
lines=[]; m.summarize(g, D, m.component_labels(), lambda s: lines.append(s))
print("\n".join(lines))
