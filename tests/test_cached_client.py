from main import CachedClient, Item, ClientInterface


class TestClient(ClientInterface):

    def get_object(self, item_id) -> Item:
        return Item(item_id, f'item_{item_id}')

    def list_objects(self) -> list[Item]:
        return [Item(item_id, f'item_{item_id}') for item_id in range(1, 10)]

    def put_object(self, item: Item) -> None:
        pass


def get_client():
    client = TestClient()
    cached_client = CachedClient(client)
    return cached_client


client = get_client()
client.get_object(1)


def test_getting():
    # cached object
    assert client.get_object(1) == Item(1, 'item_1')


client.list_objects()


def test_listing():
    # got them from the cache
    expected = [Item(item_id, f'item_{item_id}') for item_id in range(1, 10)]
    assert client.list_objects() == expected


def test_putting():
    # remove all objects from the cache
    for item in client.get_cache().values():
        client.put_object(item)
    assert not client.get_cache()
