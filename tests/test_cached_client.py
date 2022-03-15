import pytest
from main import CachedClient, db_connect, Item


def clear_table(self):
    with db_connect(self.get_filename()) as cur:
        cur.execute('DELETE FROM items')


CachedClient.clear_table = clear_table
client = CachedClient()


@pytest.fixture()
def clear_table_after_test():
    client.clear_table()


@pytest.mark.usefixtures('clear_table_after_test')
def test_cached_getting():

    for i in range(10):
        item = Item(i, f"{i}_item")
        client.put_object(item)
        client.get_object(item.id)

    test_dict = {i: Item(i, f"{i}_item") for i in range(10)}
    assert test_dict == client.get_cached_values()


@pytest.mark.usefixtures('clear_table_after_test')
def test_cache_deleting():

    for i in range(10):
        item = Item(i, f"{i}_item")
        client.put_object(item)
        client.get_object(item.id)

    client.put_object(Item(9, 'last_item'))
    test_dict = {i: Item(i, f"{i}_item") for i in range(9)}
    assert test_dict == client.get_cached_values()


@pytest.mark.usefixtures('clear_table_after_test')
def test_listing_from_first_attempt():

    CachedClient.clear_table = clear_table
    client = CachedClient()

    all_items = []
    for i in range(10):
        item = Item(i, f"{i}_item")
        all_items.append(item)
        client.put_object(item)

    assert all_items == client.list_objects()


@pytest.mark.usefixtures('clear_table_after_test')
def test_listing_from_second_attempt():

    CachedClient.clear_table = clear_table
    client = CachedClient()

    all_items = []
    for i in range(10):
        item = Item(i, f"{i}_item")
        all_items.append(item)
        client.put_object(item)

    client.list_objects()
    assert all_items == client.list_objects()
