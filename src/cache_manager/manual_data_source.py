import json
import logging
import os

from consts import CACHE_DIR
from src.cache_manager.base_data_source import BaseDataSource

logger = logging.getLogger(__name__)


class ManualDataSource(BaseDataSource):
    def get_internal_name(self, resource):
        return resource.get_name()

    def __init__(self, data_source_file_name):
        super().__init__()
        self.data_source_file_name = data_source_file_name
        with open(self._get_data_path(), "r") as f:
            logger.debug(f"loading data file {self._get_data_path()}")
            self._data_object = json.load(f)

    def get(self, resource_name: str):
        return self._data_object.get(resource_name)

    def _get_data_path(self):
        project_main_directory = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        ))
        return os.path.join(
            project_main_directory,
            CACHE_DIR,
            self.data_source_file_name + ".json"
        )

    def post_process(self, result):
        if result is None:
            return {}
        f = result.get("Father")
        if f is not None:
            result["Father"] = [f, None]
        m = result.get("Mother")
        if m is not None:
            result["Mother"] = [m, None]
        return result

    def read_entire_data_source(self):
        return self._data_object.keys()
