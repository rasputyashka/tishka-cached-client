import pytest
from main import CachedClient, Item, Sqlite


sqlite = Sqlite()
client = CachedClient()


@pytest.fixture()
def reset():
    sqlite.clear_table()
    for i in range(10):
        client.put_object(Item(i, f'{i}_item'))
    client.reset_cache()

    
@pytest.mark.usefixtures('reset')
def test_first_listing():
    expected = [Item(i, f'{i}_item') for i in range(10)]
    assert expected == client.list_objects()


@pytest.mark.usefixtures('reset')
def test_second_listing():
    expected = [Item(i, f'{i}_item') for i in range(10)]
    assert expected == client.list_objects()


@pytest.mark.usefixtures('reset')
def test_getting_object():
    expected = [Item(i, f'{i}_item') for i in range(10)]
    assert expected == [client.get_object(i) for i in range(10)]

@pytest.mark.usefixtures('reset')
def test_putting():
    expected = Item(123, '123_item')
    client.put_object(Item(1, '1_item'))
    client.put_object(Item(123, '123_item'))
    assert expected == client.get_object(123)


def teardown_module(module):
    sqlite.clear_table()
