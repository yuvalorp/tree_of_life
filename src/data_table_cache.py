import logging
import os
import pickle
from abc import ABC, abstractmethod

import src.log_config
from consts import CACHE_DIR, DATA_TABLE_VERSION, PERSON_INFO_CACHE_DIR, WIKI_PAGE_CACHE_DIR
from src.html_utils import extract_data_from_table, get_full_wiki_url, get_info_table, get_soup, get_html

logger = logging.getLogger(__name__)


class BaseCache(ABC):
    def __init__(self):
        self._cache_dir = ""

    def _get_cache_path(self, cache_name):
        project_main_directory = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        return os.path.join(
            project_main_directory,
            CACHE_DIR,
            self._cache_dir,
            cache_name.replace("/", "--"),
        )

    def _load(self, cache_name):
        with open(self._get_cache_path(cache_name), "rb") as f:
            return pickle.load(f)

    def _save_cache(self, cache_name, obj):
        with open(self._get_cache_path(cache_name), "wb") as f:
            return pickle.dump(obj, f)

    def _is_cache_exist(self, cache_name):
        return os.path.isfile(self._get_cache_path(cache_name))

    @abstractmethod
    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        pass

    def post_process(self, result):
        return result

    def get_or_load_resource(self, resource_name: str, read_cache: bool = True, write_cache: bool = True):
        result = None
        cache_exist = self._is_cache_exist(resource_name)
        if read_cache:
            if cache_exist:
                result = self._load(resource_name)
        if result is None:
            logger.debug(f"{str(self.__class__)[17:-2].split('.')[-1]} getting {resource_name}")
            result = self.get(resource_name, read_cache, write_cache)
        else:
            logger.debug(
                f"{str(self.__class__)[17:-2].split('.')[-1]} loading cache for {resource_name}"
            )
        if write_cache:
            if not cache_exist:
                self._save_cache(resource_name, result)
        return self.post_process(result)


class _WikiPageBackCache(BaseCache):
    def __init__(self):
        super().__init__()
        self._cache_dir = WIKI_PAGE_CACHE_DIR

    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        return get_html(get_full_wiki_url(resource_name))


class WikiPageCache(BaseCache):
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


class TableDataCache(BaseCache):
    def __init__(self):
        super().__init__()
        self._cache_dir = PERSON_INFO_CACHE_DIR
        self._wiki_page_cache = _WikiPageBackCache()

    def _save_cache(self, cache_name, obj):
        obj["version"] = DATA_TABLE_VERSION
        super()._save_cache(cache_name, obj)

    def _load(self, cache_name):
        cached_data = super()._load(cache_name)
        cache_is_updated = cached_data.get("version", 0) >= DATA_TABLE_VERSION
        if not cache_is_updated:
            logger.debug("cache is outdated, ignoring it")
        if cache_is_updated:
            return cached_data

    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        wiki_page = self._wiki_page_cache.get_or_load_resource(resource_name, read_cache, write_cache=False)

        infobox = get_info_table(get_soup(wiki_page))
        if infobox is None:
            return {}
        else:
            return extract_data_from_table(infobox)
