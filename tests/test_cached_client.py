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


def test_getting():
    cached_client = get_client()
    cached_client.get_object(1)
    assert cached_client.get_cache()[1] == Item(1, 'item_1')


def test_listing():
    cached_client = get_client()
    cached_client.list_objects()
    expected = [Item(item_id, f'item_{item_id}') for item_id in range(1, 10)]
    cache = cached_client.get_cache()
    is_passed = True
    for el in expected:
        if el not in cache.values():
            is_passed = False
    assert is_passed


def test_putting():
    cached_client = get_client()
    cached_client.get_object(1)
    cached_client.put_object(Item(1, 'item_1'))
    assert not cached_client.get_cache()
