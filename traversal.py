def dfs(cfg, start=None):
    start = cfg.entry if start is None else start
    if start not in cfg.blocks:
        raise ValueError
    visited = set()
    stack = [start]
    result = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        stack.extend(reversed(cfg.edges[node]))
    return result


def unreachable_blocks(cfg):
    reachable = set(dfs(cfg))
    all_blocks = set(cfg.blocks)
    return sorted(all_blocks - reachable)
