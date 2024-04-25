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
        for neighbor in reverse_graph.neighbors(current_node):
            neighbor_data = neighbor.additional_data
            gen = neighbor_data.get("gen")
            if gen is None:
                queue.append(neighbor)
                if gen == min_gen:
                    min_gen -= 1
                neighbor_data["gen"] = current_data["gen"] - 1
    for current_node in component:
        current_node.additional_data["gen"] -= min_gen
