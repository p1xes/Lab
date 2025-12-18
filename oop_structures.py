from typing import TypeVar, Generic, List, Optional

# Объявляем обобщенный тип
V = TypeVar('V')


class Queue(Generic[V]):
    """Класс Очереди (First-In-First-Out)."""

    def __init__(self) -> None:
        # Переименование внутреннее хранилище
        self._storage: List[V] = []

    def enqueue(self, value: V) -> None:
        """Добавление элемента в конец очереди"""
        self._storage.append(value)

    def dequeue(self) -> Optional[V]:
        """Извлечение элемента из начала очереди"""
        if self.is_empty():
            return None
        return self._storage.pop(0)

    def is_empty(self) -> bool:
        """Вернет True, если очередь пуста"""
        return not self._storage

    def size(self) -> int:
        """Текущее количество элементов"""
        return len(self._storage)

    def __repr__(self) -> str:
        return f"<Queue: {self._storage}>"


class Stack(Generic[V]):
    """Класс Стека (Last-In-First-Out)"""

    def __init__(self) -> None:
        self._container: List[V] = []

    def push(self, value: V) -> None:
        """Кладем элемент на вершину стека"""
        self._container.append(value)

    def pop(self) -> Optional[V]:
        """Забираем элемент с вершины стека"""
        if not self._container:
            return None
        return self._container.pop()

    def is_empty(self) -> bool:
        """Вернет True, если стек пуст"""
        return len(self._container) == 0

    def size(self) -> int:
        """Количество элементов в стеке."""
        return len(self._container)

    def __repr__(self) -> str:
        return f"<Stack: {self._container}>"


# Проверка работы
if __name__ == "__main__":
    print("Тест измененной версии")

    # 1. Очередь
    q = Queue[str]()
    q.enqueue("Клиент А")
    q.enqueue("Клиент Б")
    print(f"Очередь сейчас: {q}")

    first = q.dequeue()
    print(f"Обслужен: {first}")
    print(f"Осталось в очереди: {q.size()}")

    # 2. Стек
    s = Stack[int]()
    s.push(100)
    s.push(200)
    print(f"\nСтек сейчас: {s}")

    top = s.pop()
    print(f"Достали сверху: {top}")
    print(f"Стек пустой? -> {s.is_empty()}")