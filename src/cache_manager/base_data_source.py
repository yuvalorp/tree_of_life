from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class BaseDataSource(ABC):
    def __init__(self):
        self._class_name = str(self.__class__)[17:-2].split('.')[-1]

    def get_or_load_resource(self, resource, *args, **kwargs):
        resource_internal_name = self.get_internal_name(resource)
        if resource_internal_name is None:
            return self.post_process(None)
        logger.debug(f"{self._class_name} getting {resource_internal_name}")
        result = self.get(resource_internal_name)
        return self.post_process(result)

    @abstractmethod
    def get(self, resource_name: str):
        pass

    def post_process(self, result):
        return result

    @abstractmethod
    def get_internal_name(self, resource):
        pass
