import json
import datetime as dt
from typing import List, Dict, Any


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._born_in = born_in
        self._friends: List['Person'] = []

    def add_friend(self, friend: 'Person') -> None:
        if friend not in self._friends:
            self._friends.append(friend)
            friend._friends.append(self)

    # Публичный интерфейс
    @property
    def name(self) -> str:
        return self._name

    @property
    def born_in(self) -> dt.datetime:
        return self._born_in

    @property
    def friends(self) -> List['Person']:
        return self._friends[:]


class SafeSerializer:
    """Сериализатор, уважающий приватность"""

    def encode(self, obj: Person) -> bytes:
        graph = {}
        self._scan(obj, graph)
        # Сохраняем корневой ID, чтобы знать, с кого начинать распаковку
        return json.dumps({"root": str(id(obj)), "nodes": graph}, indent=2).encode('utf-8')

    def _scan(self, p: Person, graph: Dict) -> None:
        p_id = str(id(p))
        if p_id in graph:
            return

        graph[p_id] = {
            "n": p.name,
            "d": p.born_in.isoformat(),
            "f": [str(id(friend)) for friend in p.friends]
        }
        for friend in p.friends:
            self._scan(friend, graph)

    def decode(self, data: bytes) -> Person:
        raw = json.loads(data.decode('utf-8'))
        nodes = raw["nodes"]
        cache = {}

        # 1. Создаем объекты честно через конструктор
        for uid, props in nodes.items():
            dt_obj = dt.datetime.fromisoformat(props["d"])
            cache[uid] = Person(props["n"], dt_obj)

        # 2. Восстанавливаем связи через публичный метод
        for uid, props in nodes.items():
            person = cache[uid]
            for friend_id in props["f"]:
                friend = cache[friend_id]
                # Проверка, чтобы не добавлять дважды т.к. add_friend двусторонний
                if friend.name not in [f.name for f in person.friends]:
                    person.add_friend(friend)

        return cache[raw["root"]]


if __name__ == "__main__":
    print("ООП: Соблюдение инкапсуляции")
    p1 = Person("Ruslan", dt.datetime(2000, 1, 1))
    p2 = Person("Ivan", dt.datetime(2002, 5, 5))
    p1.add_friend(p2)

    serializer = SafeSerializer()
    data = serializer.encode(p1)
    print(f"Закодировано {len(data)} байт")

    new_p1 = serializer.decode(data)
    print(f"Восстановлен: {new_p1.name}, Друзей: {len(new_p1.friends)}")
    print(f"Имя друга: {new_p1.friends[0].name}")
