from client import DominatorTreeSSA

def main():
    print("=== Testing Dominator Tree SSA Phi Placement ===")
    cfg_nodes = ['entry', 'left', 'right', 'merge']
    cfg_edges = [('entry', 'left'), ('entry', 'right'), ('left', 'merge'), ('right', 'merge')]
    ssa = DominatorTreeSSA(cfg_nodes, cfg_edges, 'entry')

    frontiers = ssa.compute_dominance_frontiers()
    print("Dominance frontiers:", frontiers)
    phi_places = ssa.place_phi_nodes({'left'})
    print("Phi nodes for variable defined in left:", phi_places)
    assert 'merge' in phi_places

    print("Dominator Tree SSA verified successfully!")

if __name__ == '__main__':
    main()
