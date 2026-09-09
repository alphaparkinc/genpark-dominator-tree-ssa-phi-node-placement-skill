class DominatorTreeSSA:
    """Minimal SSA Phi-Node Placer using Dominance Frontiers."""
    def __init__(self, cfg_nodes, cfg_edges, entry_node):
        self.nodes = set(cfg_nodes)
        self.succs = {n: set() for n in self.nodes}
        self.preds = {n: set() for n in self.nodes}
        for u, v in cfg_edges:
            self.succs[u].add(v)
            self.preds[v].add(u)
        self.entry = entry_node

    def compute_dominance(self):
        dom = {n: set(self.nodes) for n in self.nodes}
        dom[self.entry] = {self.entry}

        changed = True
        while changed:
            changed = False
            for n in self.nodes:
                if n == self.entry:
                    continue
                pred_doms = [dom[p] for p in self.preds[n]]
                new_dom = set.intersection(*pred_doms).union({n}) if pred_doms else {n}
                if new_dom != dom[n]:
                    dom[n] = new_dom
                    changed = True
        return dom

    def compute_dominance_frontiers(self):
        dom = self.compute_dominance()
        idom = {}
        for n in self.nodes:
            if n == self.entry:
                continue
            strict_doms = dom[n] - {n}
            for d in strict_doms:
                if dom[d] == strict_doms:
                    idom[n] = d
                    break

        df = {n: set() for n in self.nodes}
        for n in self.nodes:
            if len(self.preds[n]) >= 2:
                for p in self.preds[n]:
                    runner = p
                    while runner != idom.get(n, None) and runner in dom:
                        df[runner].add(n)
                        runner = idom.get(runner, None)
        return df

    def place_phi_nodes(self, var_defs):
        df = self.compute_dominance_frontiers()
        phi_blocks = set()
        worklist = list(var_defs)

        while worklist:
            b = worklist.pop(0)
            for d in df.get(b, set()):
                if d not in phi_blocks:
                    phi_blocks.add(d)
                    if d not in var_defs:
                        worklist.append(d)
        return phi_blocks
