import networkx as nx


def _get_weakly_connected_components(graph):
    return [list(component) for component in nx.weakly_connected_components(graph)]


def find_generation(graph):
    components = _get_weakly_connected_components(graph)
    [_find_generation_connected_component(graph, n) for n in components]


def _find_generation_connected_component(graph, component):
    min_gen = 0
    reverse_graph = nx.DiGraph.reverse(graph)
    start_node = component[0]
    start_node.additional_data["gen"] = 0
    queue = [start_node]

    while len(queue) > 0:
        current_node = queue.pop(0)
        current_data = current_node.additional_data
        for neighbor in graph.neighbors(current_node):
            neighbor_data = neighbor.additional_data
            gen = neighbor_data.get("gen")
            if gen is None:
                queue.append(neighbor)
                neighbor_data["gen"] = current_data["gen"] + 1
            # else:
            #     neighbor_data["generation"] = min(current_node["generation"] + 1, neighbor_data["generation"])
        for neighbor in graph.predecessors(current_node):
            neighbor_data = neighbor.additional_data
            gen = neighbor_data.get("gen")
            if gen is None:
                queue.append(neighbor)
                if gen == min_gen:
                    min_gen -= 1
                neighbor_data["gen"] = current_data["gen"] - 1
    for current_node in component:
        current_node.additional_data["gen"] -= min_gen


def min_ancestors_knowledge_level(graph):
    leaves = [node for node in graph if graph.out_degree(node) == 0]
    graph = nx.DiGraph.reverse(graph)

    queue = []
    for node in leaves:
        node.additional_data["ancestors_knowledge_level"] = 0
        for neighbor in graph.neighbors(node):
            neighbor_data = neighbor.additional_data
            if neighbor_data.get("ancestors_knowledge_level") is None:
                neighbor_data["ancestors_knowledge_level"] = 1
                queue.append(neighbor)  # the neighbor and the ancestors_knowledge_level of the current node

    while len(queue) > 0:
        current_node = queue.pop(0)
        current_data = current_node.additional_data
        for neighbor in graph.neighbors(current_node):
            neighbor_data = neighbor.additional_data
            neighbor_knowledge_level = neighbor_data.get("ancestors_knowledge_level")
            if neighbor_knowledge_level is None:
                queue.append(neighbor)
                neighbor_data["ancestors_knowledge_level"] = current_data["ancestors_knowledge_level"] + 1
            else:
                neighbor_data["ancestors_knowledge_level"] = min(current_data["ancestors_knowledge_level"] + 1,
                                                                 neighbor_data["ancestors_knowledge_level"])
