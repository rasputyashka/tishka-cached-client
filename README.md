# tishka-cached-client

задание:
Дано: класс SomeClient с тремя методами get_object, list_objects, put_object, который посылает запросы на сервер и отдает данные.
Реализовать его кэширующую версию (CachedClient), запоминающий все полученные от сервера данные и не посылающий запрос повторно

1. Для метода get_object возвращать запомненный Item, если он уже был получен в результате list_objects или другого get_object. Если такого item_id ещё не было - запросить с сервера
2. Для метода list_objects кэшировать результат после первого вызова
3. При вызове put_object сбрасывать кэш указанного объекта, либо сразу обновлять для него кэшированное значение.

Написать тесты для добавочной функциональности класса CachedClient, не зависящие от реализации SomeClient. При этом считаем что класс 
Item
 не меняется.
Пример возможной реализации SomeClient:


import time
from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    id: int
    name: str


class SomeClient:
    def get_object(self, item_id) -> Item:
        time.sleep(1)
        return Item(item_id, "name")

    def list_objects(self) -> List[Item]:
        time.sleep(1)
        return [Item(i, "name") for i in range(10)]

    def put_object(self, item: Item) -> None:
        time.sleep(1)
