import os
import pickle
from abc import abstractmethod

from consts import CACHE_DIR
from src.cache_manager.base_cache import BaseCache


class MultiFilesBaseCache(BaseCache):
    def __init__(self):
        super().__init__()
        self._cache_dir = ""

    def _get_cache_path(self, cache_name):
        project_main_directory = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))
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
