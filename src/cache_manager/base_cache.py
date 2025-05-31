from abc import abstractmethod
from src.cache_manager.base_data_source import logger
from src.cache_manager.base_data_source import BaseDataSource


DEFAULT_CACHE_VERSION = 0


class BaseCache(BaseDataSource):
    cache_version = DEFAULT_CACHE_VERSION

    def _is_cache_updated(self, cache_obj) -> bool:
        if isinstance(cache_obj, dict):
            return cache_obj.get("version", DEFAULT_CACHE_VERSION) >= self.cache_version
        else:
            return False

    def get_or_load_resource(self, resource, read_cache: bool = True, write_cache: bool = True):
        """
        :param resource: the resource you want to get
        :param read_cache: if true will try to get it first from cache if false the cache will be ignored.
        if the cache version is below the used version the cache will be ignored
        :param write_cache: if true and the cache is outdated it will update it.
        if read_cache is false the cache will not update
        :return: the resource, return post_process(None) if failed
        """
        resource_internal_name = self.get_internal_name(resource)
        if resource_internal_name is None:
            return self.post_process(None)
        result = None
        cache_exist = self._is_cache_exist(resource_internal_name)
        is_cache_updated = False
        if read_cache:
            if cache_exist:
                cache = self._load(resource_internal_name)
                logger.info(f"{self._class_name} loading cache for {resource_internal_name}")
                is_cache_updated = self._is_cache_updated(cache)
                if is_cache_updated:
                    result = cache["object"]
                else:
                    logger.debug("cache is outdated, ignoring it")
        if result is None:
            logger.debug(f"{self._class_name} getting {resource_internal_name}")
            result = self.get(resource_internal_name, read_cache, write_cache)

        if write_cache and not is_cache_updated:
            if not cache_exist:
                cache_obj = {"version": self.cache_version, "object": result}
                self._save_cache(resource_internal_name, cache_obj)
        return self.post_process(result)

    def post_process(self, result):
        if result is None:
            return {}
        return result

    @abstractmethod
    def _load(self, cache_name):
        pass

    @abstractmethod
    def _save_cache(self, cache_name, obj):
        pass

    @abstractmethod
    def _is_cache_exist(self, cache_name) -> bool:
        pass

    @abstractmethod
    def get(self, resource_name: str, read_cache: bool, write_cache: bool):
        pass

    def get_internal_name(self, resource):
        return resource.get_wiki_url()