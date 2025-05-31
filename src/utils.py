import logging
import re
from typing import Dict, List, Union

from src.cache_manager.base_data_source import BaseDataSource
from src.html_utils import is_url_fit_name
from src.person import Person

logger = logging.getLogger(__name__)


def get_node_size(person: Person):
    return max(50 / (0.1 * person.additional_data["gen"] ** 2 + 1), 1)


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
        elif is_url_fit_name(parents_names[1], parents[1][0]):
            father = [parents_names[0], None]
            mother = [parents_names[1], parents[1][0]]
        else:
            father = [parents_names[0], None]
            mother = [parents_names[1], None]
    elif len(parents_names) == 1 and len(parents[1]) == 2:
        # probably the program couldn't separate the names
        logger.error(f"couldn't separate parents names in {parents}")
        father = [parents[1][0][6:].replace("_", " "), parents[1][0]]
        mother = [parents[1][1][6:].replace("_", " "), parents[1][1]]
    else:
        logger.error(f"coudn't find parents in {parents}")

    return father, mother


def get_year_from_key(data_dict, key):
    year = data_dict.get(key)
    if type(year) == int:
        return year
    if isinstance(year, list):
        pattern = "[0-9]{3,4}"
        match_results = re.search(pattern, year[0], re.IGNORECASE)
        if match_results is None:
            logger.error(f"coudn't find year in {year[0]}")
        else:
            year = int(match_results.group())
        return year
    else:
        logger.error(f"coudn't find {key.lower()} date in {data_dict}")


def get_person_info(data_cache: BaseDataSource, person: Person, year_born_default):
    data_dict: Dict[str, List[Union[str, None]]] = (
        data_cache.get_or_load_resource(person, write_cache=True, read_cache=True)
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
    born_year = get_year_from_key(data_dict, "Born")

    if born_year is None:
        # if the child is born for cristian family he will baptise soon after his birth
        born_year = get_year_from_key(data_dict, "Baptised")
        if born_year is None:
            born_year = year_born_default
    return mother, father, born_year
