import os

from consts import SOUP_CACHE_DIR
from src._resources.cache_utils import CacheStrategy
from src.html_utils import get_full_wiki_url
from src.html_utils import get_soup
from src._resources.resource_manager import BaseResourceManager


class SoupResourceManager(BaseResourceManager):
    def __init__(self):
        super().__init__()
        self._cache_dir = SOUP_CACHE_DIR

    def _get_cache_path(self, cache_name):
        return os.path.join(self._cache_dir, cache_name.replace("/", "--"))

    def get(
        self,
        resource_name: str,
        read_cache: bool,
        write_cache: bool,
        cache_strategy: CacheStrategy,
    ):
        return get_soup(get_full_wiki_url(resource_name))
