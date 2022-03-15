from dataclasses import dataclass
from typing import List
import sqlite3


class db_connect:

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.con = sqlite3.connect(self.filename)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, exception_type, exception_value, traceback):
        self.con.commit()
        self.cur.close()


@dataclass
class Item:
    id: int
    name: str


class Client:
    """Wrapper for sqlite"""

    __filename = 'items.db'

    def get_object(self, item_id) -> Item:
        with db_connect(self.__filename) as cur:

            query = 'SELECT id, name FROM items WHERE id = ?'
            res = cur.execute(query, (item_id,)).fetchone()
            return Item(*res)

    def list_objects(self) -> List[Item]:
        with db_connect(self.__filename) as cur:

            query = 'SELECT * FROM items'
            res = cur.execute(query)
            return [Item(id, name) for id, name in res.fetchall()]

    def put_object(self, item: Item) -> None:
        with db_connect(self.__filename) as cur:

            query = 'INSERT INTO items(id, name) VALUES (?, ?)'
            cur.execute(query, (item.id, item.name))

    def get_filename(self) -> str:
        return self.__filename


class CachedClient(Client):
    """Cached implementation for Client class"""

    def __init__(self):
        self.__cached_objects = {}
        self.__list_all_called = False

    def get_object(self, item_id) -> Item:
        if item_id not in self.__cached_objects:
            res = super().get_object(item_id)
            self.__cached_objects[item_id] = res
            return res
        return self.__cached_objects[item_id]

    def list_objects(self) -> List[Item]:
        if not self.__list_all_called:
            self.__list_all_called = True
            res = super().list_objects()
            to_cache_dict = {item.id: item for item in res}
            self.__cached_objects = {**self.__cached_objects, **to_cache_dict}
            return res
        return [item for item in self.__cached_objects.values()]

    def put_object(self, item: Item) -> None:
        try:
            del self.__cached_objects[item.id]
        except KeyError:
            pass
        finally:
            return super().put_object(item)

    def get_cached_values(self):
        return self.__cached_objects
