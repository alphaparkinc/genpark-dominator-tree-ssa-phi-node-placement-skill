import sys
import json
from client import DominatorTreeSSA

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "place_phi":
        ssa = DominatorTreeSSA(params.get("nodes", []), params.get("edges", []), params.get("entry", "entry"))
        return {"phi_blocks": list(ssa.place_phi_nodes(params.get("defs", [])))}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
