from typing import Iterable


class OrderedSet:

    def add(self, member):
        self._catalog_list = None
        self._catalog[member] = 1

    def remove(self, member):
        self._catalog_list = None
        self._catalog.pop(member)

    def __getitem__(self, index) -> any:
        if self._catalog_list is None:
            self._catalog_list = list(self._catalog.keys())
        return self._catalog_list[index]

    def __contains__(self, member) -> bool:
        return member in self._catalog

    def __bool__(self) -> bool:
        return len(self._catalog) > 0

    def __init__(self, members: Iterable = None):
        self._catalog_list = None
        self._catalog = dict()
        for m in members or []:
            self._catalog[m] = 1
