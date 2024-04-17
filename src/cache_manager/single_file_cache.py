import os
import pickle
from abc import abstractmethod

from consts import CACHE_DIR
from src.cache_manager.base_cache import BaseCache, logger


class SingleFileBaseCache(BaseCache):

    def __init__(self):
        super().__init__()
        with open(self._get_cache_path(), "rb") as f:
            logger.info(f"loading cache file for class {self._class_name}")
            self._cache_object = pickle.load(f)

    def save_cache(self):
        logger.info(f"saving cache file for class {self._class_name}")
        with open(self._get_cache_path(), "wb") as f:
            pickle.dump(self._cache_object, f)

    def _get_cache_path(self):
        project_main_directory = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))
        return os.path.join(
            project_main_directory,
            CACHE_DIR,
            self.cache_file_name + ".pkl"
        )

    def _load(self, cache_name):
        return self._cache_object[cache_name]

    def _save_cache(self, cache_name, obj):
        self._cache_object[cache_name] = obj

    def _is_cache_exist(self, cache_name):
        return cache_name in self._cache_object

    @property
    @abstractmethod
    def cache_file_name(self):
        return ""
