from main import CachedClient, Item


class TestClient:

    get_object_count = 0
    list_objects_count = 0

    def get_object(self, item_id) -> Item:
        self.get_object_count += 1
        if self.get_object_count == 1:
            return Item(item_id, f'item_{item_id}')
        else:
            raise Exception("Repeated using of get_object")

    def list_objects(self) -> list[Item]:
        self.list_objects_count += 1
        if self.list_objects_count == 1:
            return [Item(item_id, f'item_{item_id}') for item_id in range(1, 10)]
        else:
            raise Exception("Repeadted using of list_objects")

    def put_object(self, item: Item) -> None:
        pass


def get_client():
    client = TestClient()
    cached_client = CachedClient(client)
    return cached_client


def test_correct_getting():
    # cached object
    client = get_client()
    client.get_object(1)
    assert client.get_object(1) == Item(1, 'item_1')


def test_incorrect_getting():
    # cached object
    client = get_client()
    client.get_object(1)
    try:
        client.get_object(2)  # must raise Exeption:Repeadted using of get_object
    except Exception:
        assert True
    else:
        assert False


def test_putting():
    client = get_client()
    client.list_objects()
    for item in client.get_cache().values():
        client.put_object(item)
    assert not client.get_cache()
