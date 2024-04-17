import logging

import networkx as nx

import src.log_config  # noqa: F401
from person import Person
from src.cache_manager.data_table_cache import TableDataCache
from src.graph_drawer import CosmographDrawer
from src.set_plus import SetPlus
from src.utils import get_node_size, get_person_info, process_person_relative

PEOPLE_COUNT = 4
YEAR_BORN_DEFAULT = 1000

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    table_data_manager = TableDataCache()
    current_man = Person(
        "Prince George of Wales",
        "/wiki/Prince_George_of_Wales",
        {"time": 2020, "gen": 0},
    )

    checked = SetPlus()
    queue = SetPlus([current_man])
    # queue.add(Person("Prince Richard, Duke of Gloucester",
    #                  "/wiki/Prince_Richard,_Duke_of_Gloucester", {"time": 1950, "gen": 3}))

    family_graph = nx.DiGraph()  # checked+queue
    [family_graph.add_node(m, size=get_node_size(m)) for m in queue.get_list()]
    while not queue.is_empty() and len(checked) < PEOPLE_COUNT:
        current_man = queue.pop(0)
        logger.info(f"pop {current_man.get_name()}, gen: {current_man.additional_data['gen']}")
        if current_man.get_wiki_url() is not None:
            mother, father, born = get_person_info(table_data_manager, current_man.get_wiki_url(), YEAR_BORN_DEFAULT)
            logger.debug(f"{current_man.get_name()}, father: {father}, mother: {mother}")
            family_graph.nodes[current_man]["time"] = born

            process_person_relative(current_man, father, checked, queue, family_graph, relativity="parent", time=born)
            process_person_relative(current_man, mother, checked, queue, family_graph, relativity="parent", time=born)

        checked.add(current_man)

    table_data_manager.save_cache()

    drawer = CosmographDrawer()
    graph = drawer.create_graph_obj(family_graph, default_time=YEAR_BORN_DEFAULT)
    drawer.draw_graph(graph)
