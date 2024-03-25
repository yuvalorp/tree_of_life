import os
from abc import ABC, abstractmethod


class BaseDrawer(ABC):
    @staticmethod
    def _get_path(local_path):
        return os.path.join(os.path.dirname(
                os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__)))),
            local_path)

    @abstractmethod
    def create_graph_obj(self, nx_graph, **kwargs):
        pass

    @abstractmethod
    def draw_graph(self, graph, file_path):
        pass
