import logging

import networkx as nx

import src.log_config  # noqa: F401
from person import Person
from src.cache_manager.manual_data_source import ManualDataSource
from src.general_main import get_node_time, get_node_color
from src.graph_analyzing import find_generation, min_ancestors_knowledge_level
from src.graph_drawer import CosmographDrawer, PyvisDrawer
from src.utils import get_node_size, get_person_info

YEAR_BORN_DEFAULT = 1900

logger = logging.getLogger(__name__)


def process_person_relative(
        person, relative, family_graph, relativity=None, time=None
):
    if relative[0] is not None:
        if relativity == "parent":
            relative = Person(
                relative[0],
                relative[1],
                {"time": time},
            )
            family_graph.add_node(relative)
            family_graph.add_edge(person, relative)
        elif relativity == "child":
            relative = Person(
                relative[0],
                relative[1],
                {"time": time}
            )
            family_graph.add_node(relative)
            family_graph.add_edge(relative, person)
        else:
            relative = Person(
                relative[0],
                relative[1],
                {"time": time},
            )
            family_graph.add_node(relative)


if __name__ == "__main__":
    data_source = ManualDataSource("avatar")
    data = data_source.read_entire_data_source()
    logger.info(data)

    family_graph = nx.DiGraph()
    for current_man_name in data:
        current_man = Person(current_man_name)
        mother, father, born = get_person_info(data_source, current_man, YEAR_BORN_DEFAULT)
        process_person_relative(current_man, father, family_graph, relativity="parent", time=born)
        process_person_relative(current_man, mother, family_graph, relativity="parent", time=born)

    min_ancestors_knowledge_level(family_graph)
    find_generation(family_graph)

    drawer = PyvisDrawer()
    graph = drawer.create_graph_obj(family_graph,
                                    get_node_size=get_node_size,
                                    get_node_time=get_node_time,
                                    get_node_color=get_node_color)
    drawer.draw_graph(graph)
