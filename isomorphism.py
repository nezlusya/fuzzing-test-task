def find_isomorphism(first, second):
    if len(first.blocks) != len(second.blocks):
        return None

    left_nodes = sorted(first.blocks)
    right_nodes = sorted(second.blocks)
    left_out = {node: set(first.edges[node]) for node in left_nodes}
    right_out = {node: set(second.edges[node]) for node in right_nodes}

    def degree_signatures(nodes, edges):
        indegrees = {node: 0 for node in nodes}
        for targets in edges.values():
            for target in targets:
                indegrees[target] += 1
        return {node: (indegrees[node], len(edges[node]), node in edges[node]) for node in nodes}

    l_sig = degree_signatures(left_nodes, left_out)
    r_sig = degree_signatures(right_nodes, right_out)
    if sorted(l_sig.values()) != sorted(r_sig.values()):
        return None

    mapping = {}
    used = set()
    order = sorted(left_nodes, key=lambda n: (sum(l_sig[m] == l_sig[n] for m in left_nodes), n))

    def search(position):
        if position == len(order):
            return True
        node = order[position]
        for candidate in right_nodes:
            if candidate in used or l_sig[node] != r_sig[candidate]:
                continue
            if any(
                (other in left_out[node]) != (mapping[other] in right_out[candidate])
                or (node in left_out[other]) != (candidate in right_out[mapping[other]])
                for other in mapping
            ):
                continue
            mapping[node] = candidate
            used.add(candidate)
            if search(position + 1):
                return True
            used.remove(candidate)
            del mapping[node]
        return False

    return dict(mapping) if search(0) else None


def are_isomorphic(first, second):
    return find_isomorphism(first, second) is not None
