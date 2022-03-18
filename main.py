import time
from dataclasses import dataclass
from typing import List
from copy import copy


@dataclass
class Item:
    id: int
    name: str


class Client:
    def get_object(self, item_id) -> Item:
        time.sleep(1)
        return Item(item_id, f'{item_id}_item')

    def list_objects(self) -> List[Item]:
        time.sleep(1)
        return [Item(i, f'{i}_item') for i in range(10)]

    def put_object(self, item: Item) -> None:
        time.sleep(1)


class CachedClient:

    def __init__(self):
        self.client = Client()
        self.__cached_objects = {}
        self.__listed = False

    def get_object(self, item_id) -> Item:
        item = self.client.get_object(item_id)
        self.__cached_objects[item_id] = item
        return self.__cached_objects[item_id]

    def list_objects(self) -> List[Item]:
        if not self.__listed:
            items = self.client.list_objects()
            items_dict = {item.id: item for item in items}
            self.__cached_objects = {**self.__cached_objects, **items_dict}
        return self.__cached_objects.values()

    def put_object(self, item: Item) -> None:

        self.client.put_object(item)
        if item.id in self.__cached_objects:
            del self.__cached_objects[item.id]

    def get_cache(self):
        return copy(self.__cached_objects)
