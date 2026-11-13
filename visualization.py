import matplotlib.pyplot as plt
import networkx as nx


def draw_cfg(cfg, title="Граф потока управления"):
    graph = nx.DiGraph()
    graph.add_nodes_from(cfg.blocks)

    for source, targets in cfg.edges.items():
        for target in targets:
            graph.add_edge(source, target)

    if not graph.nodes:
        print("Граф пустой")
        return

    # Поиск обратных рёбер с помощью DFS
    back_edges = set()
    visited = set()
    active = set()

    def visit(node):
        visited.add(node)
        active.add(node)

        for neighbor in graph.successors(node):
            if neighbor in active:
                back_edges.add((node, neighbor))
            elif neighbor not in visited:
                visit(neighbor)

        active.remove(node)

    if cfg.entry in graph:
        visit(cfg.entry)

    for node in sorted(graph.nodes):
        if node not in visited:
            visit(node)

    # Удаляем обратные рёбра для расположения вершин
    forward_graph = graph.copy()
    forward_graph.remove_edges_from(back_edges)

    # Располагаем вершины по уровням
    levels = {node: 0 for node in graph.nodes}

    for node in nx.topological_sort(forward_graph):
        for neighbor in forward_graph.successors(node):
            levels[neighbor] = max(
                levels[neighbor],
                levels[node] + 1
            )

    by_level = {}

    for node, level in levels.items():
        by_level.setdefault(level, []).append(node)

    positions = {}

    for level, nodes in by_level.items():
        nodes.sort()

        for index, node in enumerate(nodes):
            positions[node] = (
                index - (len(nodes) - 1) / 2,
                -level
            )

    # Подписи условных переходов
    branch_labels = {}

    conditional_jumps = {
        "JG", "JGE", "JL", "JLE", "JE", "JNE"
    }

    for block_id, block in cfg.blocks.items():
        if not block.instructions:
            continue

        inst = block.instructions[-1]
        operation = inst.operation
        successors = cfg.edges[block_id]

        is_conditional = operation in conditional_jumps

        if operation == "JCC" and inst.args[0] not in ("0", "1"):
            is_conditional = True

        if is_conditional and len(successors) == 2:
            branch_labels[(block_id, successors[0])] = "if"
            branch_labels[(block_id, successors[1])] = "else"

    # Подписи вершин
    labels = {
        node: f"B{node}"
        for node in graph.nodes
    }

    forward_edges = [
        edge for edge in graph.edges
        if edge not in back_edges
    ]

    # Создаём окно для графа
    fig, ax = plt.subplots(
        figsize=(11, max(6, (max(levels.values()) + 1) * 1.2))
    )

    # Рисуем вершины
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_size=1400,
        node_color="lightblue",
        edgecolors="steelblue"
    )

    # Подписываем вершины
    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        ax=ax,
        font_size=11,
        font_weight="bold"
    )

    # Рисуем обычные рёбра
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=forward_edges,
        ax=ax,
        arrows=True,
        arrowsize=20,
        node_size=1400,
        edge_color="gray",
        width=1.6,
        connectionstyle="arc3,rad=0.05"
    )

    # Рисуем обратные рёбра циклов
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=list(back_edges),
        ax=ax,
        arrows=True,
        arrowsize=20,
        node_size=1400,
        edge_color="darkorange",
        width=2,
        style="dashed",
        connectionstyle="arc3,rad=0.3"
    )

    # Подписи if / else на рёбрах
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=branch_labels,
        ax=ax,
        font_size=10,
        font_color="darkblue",
        font_weight="bold",
        rotate=False,
        bbox={
            "boxstyle": "round,pad=0.2",
            "fc": "white",
            "ec": "none",
            "alpha": 0.9
        }
    )

    ax.set_title(title, fontsize=15)
    ax.axis("off")

    fig.tight_layout()
    plt.show()
