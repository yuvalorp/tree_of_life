import networkx as nx
from pyvis.network import Network

from consts import OUTPUT_DIR
from src.graph_drawer.base_drawer import BaseDrawer


class PyvisDrawer(BaseDrawer):
    def draw_graph(self, graph, file_path=OUTPUT_DIR):
        graph.toggle_physics(True)
        graph.show_buttons(filter_=["physics"])
        graph.show(BaseDrawer._get_path(file_path) + ".html", notebook=False)

    def create_graph_obj(
            self,
            nx_graph,
            edge_weight_transf=(lambda x: x),
            default_edge_weight=1,
            edge_scaling=False,
            get_node_size=lambda x: 1,
            **kwargs
    ):
        """
        This function convert Networkx graph to a PyVis graph format
        this is modified vertion of Network.from_nx

        :param nx_graph: The Networkx graph object that is to be translated.
        :type nx_graph: networkx.Graph instance
        :param edge_weight_transf: function to transform the edge weight for plotting
        :type edge_weight_transf: func
        :param default_edge_weight: default edge weight if not specified
        :param get_node_size: function to get the node size for plotting
        :type get_node_size: func
        """

        nt_graph = Network(directed=True)
        assert isinstance(nx_graph, nx.Graph)
        edges = nx_graph.edges(data=True)
        nodes_data = nx_graph.nodes(data=True)

        edges = [[str(e[0]), str(e[1]), e[2]] for e in edges]

        for n, n_data in nodes_data:
            nt_graph.add_node(str(n), size=get_node_size(n), **n_data)
        if len(edges) > 0:
            for e in edges:
                # if user does not pass a 'weight' argument
                if "value" not in e[2] or "width" not in e[2]:
                    if edge_scaling:
                        width_type = "value"
                    else:
                        width_type = "width"
                    if "weight" not in e[2].keys():
                        e[2]["weight"] = default_edge_weight
                    e[2][width_type] = edge_weight_transf(e[2]["weight"])
                    # replace provided weight value and pass to 'value' or 'width'
                    e[2][width_type] = e[2].pop("weight")
                nt_graph.add_edge(e[0], e[1], **e[2])
        return nt_graph
