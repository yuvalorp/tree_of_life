import networkx as nx
import pandas

from consts import OUTPUT_DIR
from src.graph_drawer.base_drawer import BaseDrawer

# https://cosmograph.app/run/
LINK_COLOR = "#EEEE00"


class CosmographDrawer(BaseDrawer):
    def draw_graph(self, graph, file_path=OUTPUT_DIR):
        graph[0].to_csv(BaseDrawer._get_path(file_path) + ".csv", index=False)
        graph[1].to_csv(BaseDrawer._get_path(file_path) + "_metadata.csv", index=False)

    def create_graph_obj(self,
                         nx_graph,
                         get_node_color=lambda x: "#111111",
                         get_node_size=lambda x: 1,
                         get_node_time=lambda x: "1 May 0", **kwargs):
        assert isinstance(nx_graph, nx.Graph)
        edges = nx_graph.edges(data=True)
        nodes_data = nx_graph.nodes(data=True)

        graph_obj = {"source": [], "target": [], "color": []}
        metadata_obj = {"id": [], "size": [], "time": [], "color": []}

        edges = [[str(e[0]), str(e[1]), e[2]] for e in edges]
        for n, n_data in nodes_data:
            metadata_obj["id"].append(n)
            metadata_obj["size"].append(get_node_size(n))
            metadata_obj["time"].append(get_node_time(n))
            metadata_obj["color"].append(get_node_color(n))
        if len(edges) > 0:
            for e in edges:
                graph_obj["source"].append(e[0])
                graph_obj["target"].append(e[1])
                graph_obj["color"].append(LINK_COLOR)
        return pandas.DataFrame(graph_obj), pandas.DataFrame(metadata_obj)
