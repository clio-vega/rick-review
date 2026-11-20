"""Re-run Lyra's OWN harness (ddf8cf6/a5230bf, branch fix/prop3-fresh-pair-eprocess) on
selected rows of her table (A) and (B), to test whether her code produces the numbers
in prop3_verify_R1000_d2.txt (which are identical to my 11-19 c2 table)."""
import sys, json, time
LYRA = sys.argv[1]           # path to code/evalue of the clone
sys.path.insert(0, LYRA)
import verify_prop3_freshpair as v
from dgp import null_dgp
from run_equicorr_puzzle import latent_factor_null_dgp
which = sys.argv[2]
t0 = time.time()
if which == 'A':
    for name, fn in [('static', null_dgp), ('latent', latent_factor_null_dgp)]:
        res = v.run_bettors(fn, 1000, 'second_order', 'cyclic')
        print(json.dumps({'row': f'{name} d2 cyclic', 'res': res, 'sec': round(time.time()-t0)}), flush=True)
else:
    for rule in ['cyclic', 'loo']:
        p = v.run_power_fixed(0.06, 500, 'second_order', rule)
        print(json.dumps({'row': f'power g=0.06 d2 {rule}', 'p': p, 'sec': round(time.time()-t0)}), flush=True)
