from main import CachedClient, Item


def test_getting_one_object():
    client = CachedClient()
    expected = Item(1, '1_item')
    client.get_object(1)  # caching result
    result = client.get_cache()[1]
    assert expected == result


def test_getting_several_items():
    client = CachedClient()
    expected = {1: Item(1, '1_item'), 2: Item(2, '2_item')}
    client.get_object(1)
    client.get_object(2)
    assert expected == client.get_cache()


def test_putting_items():
    client = CachedClient()
    expected = {1: Item(1, '1_item'), 2: Item(2, '2_item')}
    client.get_object(1)
    client.get_object(2)
    client.get_object(3)
    client.put_object(Item(3, '3_item'))
    assert expected == client.get_cache()


def test_listing_items():
    client = CachedClient()
    client.list_objects()
    cache = client.get_cache()
    for key in cache:
        client.put_object(cache[key])
    assert len(client.get_cache()) == 0
