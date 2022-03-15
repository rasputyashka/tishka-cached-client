import pytest
from main import Client, Item, db_connect


def clear_table(self):
    with db_connect(self.get_filename()) as cur:
        cur.execute("DELETE FROM items")


Client.clear_table = clear_table
client = Client()


@pytest.fixture(scope="session", autouse=True)
def clear_table_after_test():
    client.clear_table()


def test_listing():
    all_items = []
    for i in range(10):
        item = Item(i, f'{i}_item')
        all_items.append(item)
        client.put_object(item)

    assert all_items == client.list_objects()


def test_getting():
    all_items = []
    for i in range(10):
        item = Item(i, f'{i}_item')
        all_items.append(item)
        client.put_object(item)

    res_items = [client.get_object(item.id) for item in all_items]
    assert all_items == res_items
