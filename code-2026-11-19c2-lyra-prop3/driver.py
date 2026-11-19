"""driver.py -- parallel runs of freshpair_review over configs; writes results-R*.txt.
Usage: python3 -I driver.py R_valid R_power"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import freshpair_review as F


def job(cfg):
    kind, design, R, gamma, bet = cfg
    res, aux = F.run(kind, design, R, gamma=gamma, want_bettors=bet)
    return cfg, res, aux


if __name__ == '__main__':
    Rv, Rp = int(sys.argv[1]), int(sys.argv[2])
    cfgs = [(k, d, Rv, 0.0, True) for k in ('null', 'latent', 'drift')
            for d in ('d1cyc', 'd2cyc', 'd2loo')]
    cfgs += [(k, d, Rp, g, False) for k, grid in (('alt', (0.02, 0.04, 0.06, 0.10, 0.15)),
                                                   ('top3', (0.10, 0.20, 0.35)))
             for g in grid for d in ('d1cyc', 'd2cyc', 'd2loo')]
    out = []
    with Pool(4, maxtasksperchild=1) as pool:
        for cfg, res, aux in pool.imap(job, cfgs):
            out.append(dict(cfg=cfg, res=res, aux=aux))
            print(json.dumps(out[-1]), flush=True)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'results-Rv{Rv}-Rp{Rp}.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1)
    print('wrote', path)
