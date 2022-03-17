from dataclasses import dataclass
from typing import List
import sqlite3
from contextlib import contextmanager


@dataclass
class Item:
    id: int
    name: str


@contextmanager
def connect_to_db(filename: str):

    con = sqlite3.connect(filename)
    cur = con.cursor()
    try:
        yield cur
        con.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()


class Sqlite:

    __filename = 'items.db'

    def select(self, select_query: str, *args):
        with connect_to_db(self.__filename) as cur:
            return cur.execute(select_query, args).fetchall()

    def insert(self, insert_query: str, *args):
        with connect_to_db(self.__filename) as cur:
            cur.execute(insert_query, args)

    def delete(self, delete_query: str, *args):
        with connect_to_db(self.__filename) as cur:
            cur.execute(delete_query, args)

    # не знаю куда его впихнуть чтобы не манкипатчить
    def clear_table(self):
        with connect_to_db(self.__filename) as cur:
            cur.execute('DELETE FROM items')


class Client:

    def __init__(self):
        self.database = Sqlite()

    def get_object(self, item_id) -> Item:
        select_query = 'SELECT id, name FROM items WHERE id == ?'
        # [0] is fetchone
        item = self.database.select(select_query, item_id)[0]
        return Item(*item)

    def put_object(self, item: Item) -> None:
        insert_query = 'INSERT INTO items VALUES (?, ?)'
        self.database.insert(insert_query, item.id, item.name)

    def list_objects(self) -> List[Item]:
        select_query = 'SELECT * FROM items'
        items = self.database.select(select_query)
        return [Item(*it) for it in items]


class CachedClient:

    def __init__(self):
        self.database = Sqlite()
        self.__cached_data = {}
        self.__listed = False

    def get_object(self, item_id) -> Item:

        if item_id not in self.__cached_data:
            select_query = 'SELECT id, name FROM items WHERE id == ?'
            # [0] is fetchone here
            item = Item(*self.database.select(select_query, item_id)[0])
            self.__cached_data[item_id] = item
            return item
        else:
            return self.__cached_data[item_id]

    def put_object(self, item: Item) -> None:
        insert_query = 'INSERT INTO items VALUES (?, ?)'
        self.database.insert(insert_query, item.id, item.name)

        if item.id in self.__cached_data:
            del self.__cached_data[item.id]

    def list_objects(self) -> List[Item]:
        if not self.__listed:
            select_query = 'SELECT * FROM items'
            items = self.database.select(select_query)
            resp_dict = {it[0]: Item(*it) for it in items}
            self.__cached_data = {**self.__cached_data, **resp_dict}
            self.__listed = True
            return [Item(*it) for it in items]
        else:
            return list(self.__cached_data.values())

    def reset_listing(self):
        self.__listed = False

    def reset_cache(self):
        self.__cached_data = {}
        self.reset_listing()
