import json
import datetime as dt
from typing import List, Dict


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._born_in = born_in
        self._friends: List['Person'] = []

    def add_friend(self, friend: 'Person') -> None:
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)


class IntruderSerializer:
    """Сериализатор-взломщик. Игнорирует правила приличия."""

    def encode(self, obj: Person) -> bytes:
        graph = {}
        self._deep_scan(obj, graph)
        return json.dumps({"root": str(id(obj)), "nodes": graph}, indent=2).encode('utf-8')

    def _deep_scan(self, p: Person, graph: Dict) -> None:
        p_id = str(id(p))
        if p_id in graph:
            return

        # Нарушение: Прямой доступ к protected members
        graph[p_id] = {
            "_name": p._name,
            "_born_in": p._born_in.isoformat(),
            "_friends": [str(id(f)) for f in p._friends]
        }

        # Нарушение: итерация по приватному списку
        for friend in p._friends:
            self._deep_scan(friend, graph)

    def decode(self, data: bytes) -> Person:
        raw = json.loads(data.decode('utf-8'))
        nodes = raw["nodes"]
        cache = {}

        # 1. Нарушение: Создание "болванки" через __new__ (без вызова __init__)
        for uid in nodes:
            cache[uid] = Person.__new__(Person)

        # 2. Нарушение: Хирургическое вживление данных
        for uid, props in nodes.items():
            person = cache[uid]
            # Записываем атрибуты напрямую
            person._name = props["_name"]
            person._born_in = dt.datetime.fromisoformat(props["_born_in"])
            # Ручное восстановление ссылок
            person._friends = [cache[fid] for fid in props["_friends"]]

        return cache[raw["root"]]


if __name__ == "__main__":
    print("ООП: Нарушение инкапсуляции")
    p1 = Person("Hacker", dt.datetime(1999, 9, 9))
    p2 = Person("Victim", dt.datetime(1990, 1, 1))
    p1.add_friend(p2)

    serializer = IntruderSerializer()
    data = serializer.encode(p1)

    new_p1 = serializer.decode(data)
    print(f"Восстановлен (через взлом): {new_p1._name}")
    print(f"Друг (приватное поле): {new_p1._friends[0]._name}")
