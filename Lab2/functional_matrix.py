from typing import List, Union, TypeAlias

# Объявляем синонимы типов для чистоты кода
MatrixData = List[List[float]]
Scalar = Union[int, float]


def get_shape(m: MatrixData) -> tuple[int, int]:
    """Возвращает (строки, столбцы)"""
    return len(m), len(m[0]) if m else 0


def create_matrix(data: List[List[float]]) -> MatrixData:
    """Создает матрицу (валидация и копирование)"""
    if not data:
        return []
    width = len(data[0])
    for r in data:
        if len(r) != width:
            raise ValueError("Некорректная матрица: разная длина строк")
    return [row[:] for row in data]


def mat_add(a: MatrixData, b: MatrixData) -> MatrixData:
    """Сложение двух матриц"""
    if get_shape(a) != get_shape(b):
        raise ValueError("Размеры матриц должны совпадать")

    # List comprehension для сложения
    return [[x + y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(a, b)]


def mat_transpose(m: MatrixData) -> MatrixData:
    """Транспонирование матрицы"""
    # Functional magic: zip распаковывает столбцы в строки
    return [list(col) for col in zip(*m)]


def mat_mul(a: MatrixData, b: Union[MatrixData, Scalar]) -> MatrixData:
    """Умножение: Матрица * Матрица ИЛИ Матрица * Число"""

    # Вариант 1: Умножение на число
    if isinstance(b, (int, float)):
        return [[x * b for x in row] for row in a]

    # Вариант 2: Умножение матриц
    rows_a, cols_a = get_shape(a)
    rows_b, cols_b = get_shape(b)

    if cols_a != rows_b:
        raise ValueError(f"Ошибка размерности: {cols_a} != {rows_b}")

    # Транспонируем B заранее, чтобы удобно идти по строкам
    b_t = mat_transpose(b)

    return [
        [sum(x * y for x, y in zip(row_a, row_b_t)) for row_b_t in b_t]
        for row_a in a
    ]


def mat_det(m: MatrixData) -> float:
    """Вычисление определителя (Determinant)"""
    rows, cols = get_shape(m)
    if rows != cols:
        raise ValueError("Нужна квадратная матрица")

    # Простые случаи
    if rows == 1: return m[0][0]
    if rows == 2: return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    # Общий случай (рекурсия)
    det = 0.0
    first_row = m[0]
    for i, val in enumerate(first_row):
        # Формируем минор без 0-й строки и i-го столбца
        minor = [row[:i] + row[i + 1:] for row in m[1:]]
        sign = 1 if i % 2 == 0 else -1
        det += sign * val * mat_det(minor)

    return det


if __name__ == "__main__":
    print(" Тест Функциональный")
    mx1 = create_matrix([[1.0, 2.0], [2.0, 3.0]])
    mx2 = create_matrix([[2.0, 5.0], [7.0, 9.0]])

    print("Сумма:", mat_add(mx1, mx2))
    print("Трансп:", mat_transpose(mx1))
    print("Умнож (Матрица):", mat_mul(mx1, mx2))
    print("Умнож (Скаляр):", mat_mul(mx1, 10))
    print("Дет:", mat_det(mx1))
