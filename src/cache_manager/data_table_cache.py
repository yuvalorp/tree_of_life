import logging

from consts import PERSON_INFO_CACHE_FILE, WIKI_PAGE_CACHE_DIR
from src.cache_manager.multi_files_cache import MultiFilesBaseCache
from src.cache_manager.single_file_cache import SingleFileBaseCache
from src.html_utils import (extract_data_from_table, get_full_wiki_url,
                            get_html, get_info_table, get_soup)

logger = logging.getLogger(__name__)


class _WikiPageBackCache(MultiFilesBaseCache):
    def __init__(self):
        super().__init__()
        self._cache_dir = WIKI_PAGE_CACHE_DIR

    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        return get_html(get_full_wiki_url(resource_name))


class WikiPageCache(MultiFilesBaseCache):
    def __init__(self):
        super().__init__()
        self._cache_dir = WIKI_PAGE_CACHE_DIR
        self._wiki_page_cache = _WikiPageBackCache()

    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        return self._wiki_page_cache.get_or_load_resource(
            resource_name, read_cache, write_cache
        )

    def post_process(self, result):
        infobox = get_info_table(get_soup(result))
        if infobox is None:
            return {}
        else:
            return extract_data_from_table(infobox)


class TableDataCache(SingleFileBaseCache):
    def __init__(self):
        super().__init__()
        self._wiki_page_cache = _WikiPageBackCache()

    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        wiki_page = self._wiki_page_cache.get_or_load_resource(resource_name, read_cache, write_cache=False)

        infobox = get_info_table(get_soup(wiki_page))
        if infobox is None:
            return {}
        else:
            return extract_data_from_table(infobox)

    @property
    def cache_file_name(self):
        return PERSON_INFO_CACHE_FILE
