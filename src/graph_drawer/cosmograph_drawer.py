import networkx as nx
import pandas

from consts import OUTPUT_DIR
from src.graph_drawer.base_drawer import BaseDrawer

# https://cosmograph.app/run/


class CosmographDrawer(BaseDrawer):
    def draw_graph(self, graph, file_path=OUTPUT_DIR):
        graph[0].to_csv(BaseDrawer._get_path(file_path) + ".csv", index=False)
        graph[1].to_csv(BaseDrawer._get_path(file_path) + "_metadata.csv", index=False)

    def create_graph_obj(self, nx_graph, default_time=1000, **kwargs):
        assert isinstance(nx_graph, nx.Graph)
        edges = nx_graph.edges(data=True)
        nodes_data = nx_graph.nodes(data=True)

        graph_obj = {"source": [], "target": []}
        metadata_obj = {"id": [], "size": [], "time": []}

        edges = [[str(e[0]), str(e[1]), e[2]] for e in edges]
        for n, n_data in nodes_data:
            metadata_obj["id"].append(n)
            metadata_obj["size"].append(n_data["size"] / 2)
            metadata_obj["time"].append(f"1 March {n_data.get('time', default_time)}")
        if len(edges) > 0:
            for e in edges:
                graph_obj["source"].append(e[0])
                graph_obj["target"].append(e[1])
        return pandas.DataFrame(graph_obj), pandas.DataFrame(metadata_obj)
