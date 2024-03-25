import os

from consts import PERSON_INFO_CACHE_DIR
from src._resources.cache_utils import CacheStrategy
from src.html_utils import extract_data_from_table, get_info_table
from src._resources.resource_manager import BaseResourceManager
from src._resources.soup_resource_manager import SoupResourceManager


class TableDataResourceManager(BaseResourceManager):
    def __init__(self):
        super().__init__()
        self._cache_dir = PERSON_INFO_CACHE_DIR
        self._soup_manager = SoupResourceManager()

    def _get_cache_path(self, cache_name):
        return os.path.join(self._cache_dir, cache_name.replace("/", "--"))

    def get(
        self,
        resource_name: str,
        read_cache: bool,
        write_cache: bool,
        cache_strategy: CacheStrategy,
    ):
        if CacheStrategy == CacheStrategy.TOP:
            soup = self._soup_manager.get_or_load_resource(
                resource_name,
                read_cache,
                write_cache=False,
                cache_strategy=cache_strategy,
            )
        else:
            soup = self._soup_manager.get_or_load_resource(
                resource_name,
                read_cache,
                write_cache=write_cache,
                cache_strategy=cache_strategy,
            )

        infobox = get_info_table(soup, resource_name)
        if infobox is None:
            return {}
        else:
            return extract_data_from_table(infobox)
