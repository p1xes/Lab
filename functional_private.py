import json
import datetime as dt
from typing import List, Dict, Any


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._born_in = born_in
        self._friends: List['Person'] = []

    def add_friend(self, friend: 'Person') -> None:
        self._friends.append(friend)
        friend._friends.append(self)

    # Геттеры для функционального подхода
    @property
    def name(self) -> str: return self._name

    @property
    def born_in(self) -> dt.datetime: return self._born_in

    @property
    def friends(self) -> List['Person']: return self._friends[:]


def serialize_safe(obj: Person) -> bytes:
    """Функция сериализации (Safe Mode)"""
    registry = {}

    def visit(p: Person):
        p_id = str(id(p))
        if p_id in registry: return

        # Только публичные поля
        registry[p_id] = {
            "name": p.name,
            "born_in": p.born_in.isoformat(),
            "friends_ids": [str(id(f)) for f in p.friends]
        }
        for friend in p.friends:
            visit(friend)

    visit(obj)
    return json.dumps({"root": str(id(obj)), "data": registry}, indent=2).encode('utf-8')


def deserialize_safe(data: bytes) -> Person:
    """Функция десериализации (Safe Mode)"""
    payload = json.loads(data.decode('utf-8'))
    registry = payload["data"]
    instances = {}

    # 1. Создание через конструктор
    for pid, info in registry.items():
        born = dt.datetime.fromisoformat(info["born_in"])
        instances[pid] = Person(info["name"], born)

    # 2. Связывание
    for pid, info in registry.items():
        curr = instances[pid]
        for fid in info["friends_ids"]:
            friend = instances[fid]
            # Избегаем дублирования
            if friend not in curr.friends:
                curr.add_friend(friend)

    return instances[payload["root"]]


if __name__ == "__main__":
    print("Соблюдение инкапсуляции")
    p1 = Person("FuncUser", dt.datetime(2005, 5, 5))
    encoded = serialize_safe(p1)
    decoded = deserialize_safe(encoded)
    print(f"Результат: {decoded.name}")