import json
import datetime as dt
from typing import List, Dict


class Person:
    def __init__(self, name: str, born_in: dt.datetime) -> None:
        self._name = name
        self._born_in = born_in
        self._friends: List['Person'] = []

    def add_friend(self, friend: 'Person') -> None:
        self._friends.append(friend)
        friend._friends.append(self)


def serialize_broken(obj: Person) -> bytes:
    """Сериализация через интроспекцию __dict__ (Unsafe)"""
    registry = {}

    def visit(p: Person):
        p_id = str(id(p))
        if p_id in registry: return

        state = p.__dict__.copy()

        # Адаптируем данные для JSON
        state['_born_in'] = state['_born_in'].isoformat()
        state['_friends'] = [str(id(f)) for f in state['_friends']]

        registry[p_id] = state

        for friend in p._friends:
            visit(friend)

    visit(obj)
    return json.dumps({"root": str(id(obj)), "data": registry}, indent=2).encode('utf-8')


def deserialize_broken(data: bytes) -> Person:
    """Десериализация в обход конструктора"""
    payload = json.loads(data.decode('utf-8'))
    registry = payload["data"]
    instances = {}

    # 1. Allocator: выделяем память без инициализации
    for pid in registry:
        instances[pid] = object.__new__(Person)

    # 2. Injector: впрыскиваем данные
    for pid, state in registry.items():
        obj = instances[pid]
        obj._name = state['_name']
        obj._born_in = dt.datetime.fromisoformat(state['_born_in'])
        # Восстанавливаем ссылки из ID
        obj._friends = [instances[fid] for fid in state['_friends']]

    return instances[payload["root"]]


if __name__ == "__main__":
    print("Нарушение инкапсуляции")
    p1 = Person("FuncHacker", dt.datetime(2010, 10, 10))
    p2 = Person("Friend", dt.datetime(2011, 11, 11))
    p1.add_friend(p2)

    encoded = serialize_broken(p1)
    decoded = deserialize_broken(encoded)

    # Доказываем, что данные на месте
    print(f"Имя: {decoded._name}")  # Прямой доступ
    print(f"Друг: {decoded._friends[0]._name}")
