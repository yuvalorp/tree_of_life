import logging
import os
import pickle
from abc import ABC, abstractmethod

from consts import CACHE_DIR
from src._resources.cache_utils import CacheStrategy

logger = logging.getLogger(__name__)


class BaseResourceManager(ABC):
    def __init__(self):
        self._cache_dir = ""

    def _get_cache_path(self, cache_name):
        project_main_directory = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return os.path.join(
            project_main_directory, CACHE_DIR, self._cache_dir, cache_name
        )

    def _load_if_exist(self, cache_name):
        with open(self._get_cache_path(cache_name), "rb") as f:
            return pickle.load(f)

    def _save_cache(self, cache_name, obj):
        with open(self._get_cache_path(cache_name), "wb") as f:
            return pickle.dump(obj, f)

    def _is_cache_exist(self, cache_name):
        return os.path.isfile(self._get_cache_path(cache_name))

    @abstractmethod
    def get(
        self,
        resource_name: str,
        read_cache: bool,
        write_cache: bool,
        cache_strategy: CacheStrategy,
    ):
        pass

    def get_or_load_resource(
        self,
        resource_name: str,
        read_cache: bool = True,
        write_cache: bool = True,
        cache_strategy: CacheStrategy = CacheStrategy.TOP,
    ):
        result = None
        cache_exist = self._is_cache_exist(resource_name)
        if read_cache:
            if cache_exist:
                result = self._load_if_exist(resource_name)
        if result is None:
            logger.debug(
                f"{str(self.__class__)[17:-2].split('.')[-1]} getting {resource_name}"
            )
            result = self.get(resource_name, read_cache, write_cache, cache_strategy)
        else:
            logger.debug(
                f"{str(self.__class__)[17:-2].split('.')[-1]} loading cache for {resource_name}"
            )
        if write_cache:
            if not cache_exist:
                self._save_cache(resource_name, result)
        return result
