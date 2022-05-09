import time
from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    id: int
    name: str


class ClientInterface:
    def get_object(self, item_id) -> Item:
        raise NotImplementedError()

    def list_objects(self) -> List[Item]:
        raise NotImplementedError()

    def put_object(self, item: Item) -> None:
        raise NotImplementedError()


class Client(ClientInterface):
    def get_object(self, item_id):
        time.sleep(1)
        return Item(item_id, f'{item_id}_item')

    def list_objects(self) -> List[Item]:
        time.sleep(1)
        return [Item(i, f'{i}_item') for i in range(10)]

    def put_object(self, item: Item) -> None:
        time.sleep(1)


class CachedClient:

    def __init__(self, decoratee):
        self.decoratee = decoratee
        self.cache = {}
        self.listed = False

    def get_object(self, item_id):
        if item_id not in self.cache:
            self.cache[item_id] = self.decoratee.get_object(item_id)
        return self.cache[item_id]

    def list_objects(self):
        if not self.listed:
            self.listed = True
            items = self.decoratee.list_objects()
            self.cache.update({item.id: item for item in items})
        return list(self.cache.values())

    def put_object(self, item):
        self.decoratee.put_object(item)
        if item.id in self.cache:
            del self.cache[item.id]

    def get_cache(self) -> dict[int, Item]:
        return self.cache.copy()
