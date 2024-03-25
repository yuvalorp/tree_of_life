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
        node_size_transf=(lambda x: x),
        edge_weight_transf=(lambda x: x),
        default_node_size=10,
        default_edge_weight=1,
        edge_scaling=False,
        **kwargs
    ):
        """
        This function takes an exisitng Networkx graph and translates
        it to a PyVis graph format that can be accepted by the VisJs
        API in the Jinja2 template. This operation is done in place.
        this is modified vertion of Network.from_nx

        :param nx_graph: The Networkx graph object that is to be translated.
        :type nx_graph: networkx.Graph instance
        :param node_size_transf: function to transform the node size for plotting
        :type node_size_transf: func
        :param edge_weight_transf: function to transform the edge weight for plotting
        :type edge_weight_transf: func
        :param default_node_size: default node size if not specified
        :param default_edge_weight: default edge weight if not specified
        >>> nx_graph = nx.cycle_graph(10)
        >>> nx_graph.nodes[1]['title'] = 'Number 1'
        >>> nx_graph.nodes[1]['group'] = 1
        >>> nx_graph.nodes[3]['title'] = 'I belong to a different group!'
        >>> nx_graph.nodes[3]['group'] = 10
        >>> nx_graph.add_node(20, size=20, title='couple', group=2)
        >>> nx_graph.add_node(21, size=15, title='couple', group=2)
        >>> nx_graph.add_edge(20, 21, weight=5)
        >>> nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)
        >>> nt = Network("500px", "500px")
        # populates the nodes and edges data structures
        >>> nt.from_nx(nx_graph)
        >>> nt.show("nx.html")
        """
        nt_graph = Network()
        assert isinstance(nx_graph, nx.Graph)
        edges = nx_graph.edges(data=True)
        nodes_data = nx_graph.nodes(data=True)
        isolates = nx.isolates(nx_graph)

        edges = [[str(e[0]), str(e[1]), e[2]] for e in edges]
        nodes = {}
        for n, n_data in nodes_data:
            nodes[str(n)] = n_data
        isolates = [str(i) for i in isolates]

        if len(edges) > 0:
            for e in edges:
                if "size" not in nodes[e[0]].keys():
                    nodes[e[0]]["size"] = default_node_size
                nodes[e[0]]["size"] = int(node_size_transf(nodes[e[0]]["size"]))
                if "size" not in nodes[e[1]].keys():
                    nodes[e[1]]["size"] = default_node_size
                nodes[e[1]]["size"] = int(node_size_transf(nodes[e[1]]["size"]))
                nt_graph.add_node(e[0], **nodes[e[0]])
                nt_graph.add_node(e[1], **nodes[e[1]])

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

        for node in isolates:
            if "size" not in nodes[node].keys():
                nodes[node]["size"] = default_node_size
            nt_graph.add_node(node, **nodes[node])
        return nt_graph
