from copy import copy
from typing import Iterable, Optional


class SetPlus:
    def __init__(self, object_list: Optional[Iterable] = None):
        if object_list is None:
            object_list = []
        self._object_list = list(object_list)

    def get_list(self):
        return copy(self._object_list)

    def simple_add(self, obj):
        for x in self._object_list:
            if x == obj:
                return
        self._object_list.append(obj)

    def add(self, obj):
        i = 0
        for x in self._object_list:
            if x == obj:
                x.update(obj)
                return i
            i += 1
        self._object_list.append(obj)
        return -1

    def index(self, obj):
        i = 0
        for x in self._object_list:
            if x == obj:
                return i
            i += 1
        return -1

    def __contains__(self, obj):
        for x in self._object_list:
            if x == obj:
                return True
        return False

    def __len__(self):
        return len(self._object_list)

    def is_empty(self):
        return self._object_list == []

    def pop(self, index=None):
        if index is None:
            return self._object_list.pop()
        else:
            return self._object_list.pop(index)

    def pop_smallest(self, key):
        min_item = min(self._object_list, key=key)
        self._object_list.remove(min_item)
        return min_item
