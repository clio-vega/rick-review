cd /home/clio/projects/reviews/code-1024c2-thmI
python3 -u window.py 6 2>&1 | grep -E "THEOREM|m=[0-9] (LG|OG)|\(.*s\)"
echo "== NEGATIVE CONTROL: shift the window by +-1; both arms MUST fire =="
python3 -u -c "
import window
for m in (3,4):
    for (typ,sh,vb,nb) in window.negctl(m):
        v='FIRES' if (vb+nb)>0 else '*** SILENT -- test cannot fail ***'
        print(f'  m={m} {typ} window shifted {sh:+d}: vanishing-violations {vb}, positivity-violations {nb}  -> {v}')
" 2>&1 | grep -E "m=[0-9] (LG|OG)"
