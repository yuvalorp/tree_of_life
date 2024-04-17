import logging
import re
from typing import Dict, List, Union

from src.cache_manager.base_cache import BaseCache
from src.html_utils import is_url_fit_name
from src.person import Person

logger = logging.getLogger(__name__)


def get_node_size(person: Person):
    return max(50 / (0.05 * person.additional_data["gen"] ** 2 + 1), 2)


def process_parents_key(parents):
    father = [None, None]
    mother = [None, None]
    parents_names = [x.strip() for x in parents[0].split("\n")]
    parents_names = [
        x
        for x in parents_names
        if len(x) > 2 and x not in ("(father)", "(mother)") and not x.endswith(".")
    ]  # the len>2 is for protection
    if len(parents_names) == 2 and parents[1] is None:
        father = [parents_names[0], None]
        mother = [parents_names[1], None]
    elif len(parents_names) == 2 and len(parents[1]) == 2:
        father = [parents_names[0], parents[1][0]]
        mother = [parents_names[1], parents[1][1]]
    elif len(parents_names) == 1 and len(parents[1]) == 1:
        father = [parents_names[0], parents[1][0]]
    elif len(parents_names) == 2 and len(parents[1]) == 1:
        if is_url_fit_name(parents_names[0], parents[1][0]):
            father = [parents_names[0], parents[1][0]]
            mother = [parents_names[1], None]
        elif is_url_fit_name(parents_names[0], parents[1][0]):
            father = [parents_names[0], None]
            mother = [parents_names[1], parents[1][0]]
        else:
            logger.error(f"coudn't find parents in {parents}")
    else:
        logger.error(f"coudn't find parents in {parents}")

    return father, mother


def get_born_year(data_dict, year_born_default):
    born = data_dict.get("Born", year_born_default)
    if isinstance(born, list):
        pattern = "[0-9]{3,4}"
        match_results = re.search(pattern, born[0], re.IGNORECASE)
        if match_results is None:
            logger.error(f"coudn't find year in {born[0]}")
            born = year_born_default
        else:
            born = int(match_results.group())
    else:
        logger.error(f"coudn't find born date in {data_dict}")
    return born


def get_person_info(table_data_manager: BaseCache, internal_url, year_born_default):
    data_dict: Dict[str, List[Union[str, None]]] = (
        table_data_manager.get_or_load_resource(internal_url, write_cache=True, read_cache=True)
    )

    mother = data_dict.get("Mother", [None, None])
    father = data_dict.get("Father", [None, None])
    if father[0] is None and mother[0] is None:
        parents = data_dict.get("Parents", data_dict.get("Parent(s)"))
        if parents is not None:
            father, mother = process_parents_key(parents)
    else:
        mother[1] = mother[1][0] if mother[1] is not None else mother[1]
        father[1] = father[1][0] if father[1] is not None else father[1]

    return mother, father, get_born_year(data_dict, year_born_default)


def process_person_relative(
        person, relative, checked, queue, family_graph, relativity=None, time=None
):
    if relative[0] is not None:
        if relativity == "parent":
            relative = Person(
                relative[0],
                relative[1],
                {"time": time, "gen": person.additional_data["gen"] + 1},
            )
        else:
            relative = Person(
                relative[0],
                relative[1],
                {"time": time, "gen": person.additional_data["gen"]},
            )

        # if we will not have the birth year of the man we will use the birth year of his relative
        family_graph.add_node(relative, size=get_node_size(relative), time=time)
        family_graph.add_edge(person, relative)
        if relative not in checked and relative not in queue:
            queue.add(relative)
