from typing import TypeVar, List, Optional, NoReturn

E = TypeVar('E')

# Логика Очереди (Queue)

def init_queue() -> List[E]:
    """Инициализирует пустую очередь"""
    return []


def queue_add(q: List[E], value: E) -> None:
    """Добавляет элемент в очередь. Изменяет переданный список напрямую (без копирования)"""
    q.append(value)


def queue_take(q: List[E]) -> Optional[E]:
    """Извлекает первый элемент из очереди. Возвращает None, если очередь пуста"""
    if not q:
        return None
    # Удаляем нулевой элемент.
    return q.pop(0)


def queue_check_empty(q: List[E]) -> bool:
    """Возвращает True, если очередь пуста"""
    return not q


def queue_length(q: List[E]) -> int:
    """Возвращает текущую длину очереди"""
    return len(q)


#Логика Стека (Stack)

def init_stack() -> List[E]:
    """Инициализирует пустой стек"""
    return []


def stack_push(s: List[E], value: E) -> None:
    """ Кладет элемент на вершину стека. Работает in-place (изменяет переданный список)."""
    s.append(value)


def stack_pop(s: List[E]) -> Optional[E]:
    """Снимает элемент с вершины стека. Возвращает None, если стек пуст. """
    if not s:
        return None
    return s.pop()


def stack_check_empty(s: List[E]) -> bool:
    """Возвращает True, если стек пуст."""
    return len(s) == 0


def stack_height(s: List[E]) -> int:
    """Возвращает высоту стека."""
    return len(s)


# Демонстрация
if __name__ == "__main__":
    print("Функциональная реализация (Mutable/In-Place)\n")

    # 1. Тест Очереди
    my_queue: List[str] = init_queue()
    print(f"Очередь создана: {my_queue}")

    queue_add(my_queue, "Первый")
    queue_add(my_queue, "Второй")
    print(f"Очередь после добавления: {my_queue} | Размер: {queue_length(my_queue)}")

    elem = queue_take(my_queue)
    print(f"Забрали: {elem}")
    print(f"Очередь сейчас: {my_queue}")

    # 2. Тест Стека
    print("\nТест Стека\n")
    my_stack: List[int] = init_stack()

    stack_push(my_stack, 100)
    stack_push(my_stack, 200)
    stack_push(my_stack, 300)
    print(f"Стек заполнен: {my_stack}")

    top_val = stack_pop(my_stack)
    print(f"Сняли верхушку: {top_val}")
    print(f"Стек после pop: {my_stack}")
    print(f"Пустой ли стек? -> {stack_check_empty(my_stack)}")
