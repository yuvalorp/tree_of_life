import logging

import networkx as nx

import src.log_config  # noqa: F401
from person import Person
from src.cache_manager.data_table_cache import TableDataCache
from src.graph_analyzing import find_generation, min_ancestors_knowledge_level
from src.graph_drawer import CosmographDrawer
from src.set_plus import SetPlus
from src.utils import get_node_size, get_person_info

PEOPLE_COUNT = 4
YEAR_BORN_DEFAULT = 1000

logger = logging.getLogger(__name__)


def get_node_time(x):
    return f"1 May {x.additional_data.get('time', YEAR_BORN_DEFAULT)}"


def get_node_color(x):
    nodes_color_palette = ("#B6F3E9", "#FEEEFB", "#F3D6DA", "#D2C2DE", "#58909D", "#104547", "#252323")
    return nodes_color_palette[x.additional_data.get("ancestors_knowledge_level", 0)]


def process_person_relative(
        person, relative, checked, queue, family_graph, relativity=None, time=None
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

        if relative not in checked and relative not in queue:
            queue.add(relative)


if __name__ == "__main__":
    table_data_manager = TableDataCache()
    checked = SetPlus()
    queue = SetPlus([])

    queue.add(Person("Prince George of Wales",
                     "/wiki/Prince_George_of_Wales", {"time": 2020}))
    queue.add(Person("Prince Richard, Duke of Gloucester",
                     "/wiki/Prince_Richard,_Duke_of_Gloucester", {"time": 1950}))

    family_graph = nx.DiGraph()  # checked+queue
    [family_graph.add_node(m) for m in queue.get_list()]
    while not queue.is_empty() and len(checked) < PEOPLE_COUNT:
        current_man = queue.pop(0)
        if current_man.get_wiki_url() is not None:
            mother, father, born = get_person_info(table_data_manager, current_man.get_wiki_url(), YEAR_BORN_DEFAULT)
            logger.debug(f"{current_man.get_name()}, father: {father}, mother: {mother}")
            current_man.additional_data["time"] = born

            process_person_relative(current_man, father, checked, queue, family_graph, relativity="parent", time=born)
            process_person_relative(current_man, mother, checked, queue, family_graph, relativity="parent", time=born)

        checked.add(current_man)

    table_data_manager.save_cache()

    min_ancestors_knowledge_level(family_graph)
    find_generation(family_graph)

    drawer = CosmographDrawer()
    graph = drawer.create_graph_obj(family_graph,
                                    get_node_size=get_node_size,
                                    get_node_time=get_node_time,
                                    get_node_color=get_node_color)
    drawer.draw_graph(graph)
