"""OEIS absence check with the HTTP status inspected, not just the body.
A working pipe returning empty looks exactly like an empty field."""
import urllib.request, urllib.error, json, time

def probe(name, terms, nterms):
    q = ",".join(str(x) for x in terms[:nterms])
    url = "https://oeis.org/search?q=%s&fmt=json" % urllib.parse.quote(q)
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'clio-peer-review/1.0'})
        with urllib.request.urlopen(req, timeout=45) as r:
            status = r.status
            body = r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        print("  %-4s n=%-2d HTTP %s  (HTTPError)  body[:120]=%r" % (name,nterms,e.code,e.read()[:120]))
        return None
    except Exception as e:
        print("  %-4s n=%-2d TRANSPORT FAILURE: %r" % (name,nterms,e))
        return None
    print("  %-4s n=%-2d HTTP %s  bytes=%d" % (name,nterms,status,len(body)), end="")
    try:
        j = json.loads(body)
    except Exception:
        print("   -> body is not JSON; first 200 chars: %r" % body[:200]); return None
    if j is None:
        print("   -> JSON null  == NO MATCH"); return []
    if isinstance(j, dict):
        cnt=j.get('count'); res=j.get('results') or []
        print("   -> count=%s  hits=%s" % (cnt,[x.get('number') for x in res][:8])); return res
    print("   -> %d hit(s): %s" % (len(j), [x.get('number') for x in j][:8])); return j

# CONTROL: a sequence that is certainly IN OEIS.  If this returns nothing,
# the instrument is broken and every "absent" reading is meaningless.
print("=== POSITIVE CONTROL (Catalan numbers, must be found) ===")
probe("cat",[1,1,2,5,14,42,132,429,1430],9)
print("=== POSITIVE CONTROL 2 (A003319, connected permutations, from AGGSZ) ===")
probe("A003319",[1,1,3,13,71,461,3447],7)

b=[3,27,417,7851,164124,3661389,85384566,2056373739,50751637140,1276862920140,32626363346505,844375375808301]
a=[3,18,282,5268,109647,2438928,56758176,1364824620,33643660620,845633502606,21590775239850,558411335278644]
p=[3,21,344,6447,134571,2995655,69761697,1678307754,41386815905,1040573158494,26574621911472,687454232433863]
print()
print("=== RICK'S THREE SEQUENCES ===")
for nm,seq in (("b",b),("a",a),("p",p)):
    for n in (5,8,12):
        probe(nm,seq,n); time.sleep(1.5)
