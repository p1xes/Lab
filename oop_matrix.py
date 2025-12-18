from typing import List, Union, Optional

# Определяем тип для содержимого матрицы (числа)
Num = Union[int, float]


class Matrix:
    """Класс Matrix с реализацией основных математических операций"""

    def __init__(self, grid: List[List[Num]]) -> None:
        # Проверяем валидность при создании
        self._check_consistency(grid)
        # Создаем глубокую копию данных, чтобы изменения извне не ломали матрицу
        self._values = [row[:] for row in grid]

    @property
    def shape(self) -> tuple[int, int]:
        """Возвращает размерность матрицы (строки, столбцы)"""
        if not self._values:
            return 0, 0
        return len(self._values), len(self._values[0])

    @staticmethod
    def _check_consistency(grid: List[List[Num]]) -> None:
        """Проверяет, что матрица прямоугольная"""
        if not grid:
            return
        width = len(grid[0])
        if any(len(row) != width for row in grid):
            raise ValueError("Матрица должна иметь строки одинаковой длины")

    def __str__(self) -> str:
        return '\n'.join([' '.join(f"{x:5.1f}" for x in row) for row in self._values])

    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Оператор сложения (+)"""
        if self.shape != other.shape:
            raise ValueError(f"Размерности не совпадают: {self.shape} != {other.shape}")

        # Складываем поэлементно, используя zip
        new_grid = [
            [a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self._values, other._values)
        ]
        return Matrix(new_grid)

    def __mul__(self, other: Union['Matrix', Num]) -> 'Matrix':
        """Оператор умножения (*). Работает и со скаляром, и с матрицей"""

        # 1. Умножение на число (Скаляр)
        if isinstance(other, (int, float)):
            new_grid = [[x * other for x in row] for row in self._values]
            return Matrix(new_grid)

        # 2. Умножение на матрицу
        elif isinstance(other, Matrix):
            rows_a, cols_a = self.shape
            rows_b, cols_b = other.shape

            if cols_a != rows_b:
                raise ValueError(f"Нельзя умножить: столбцов в A ({cols_a}) != строк в B ({rows_b})")

            other_t = list(zip(*other._values))

            result = [
                [sum(a * b for a, b in zip(row, col)) for col in other_t]
                for row in self._values
            ]
            return Matrix(result)

        return NotImplemented

    def transpose(self) -> 'Matrix':
        """Возвращает транспонированную матрицу"""
        transposed_data = [list(col) for col in zip(*self._values)]
        return Matrix(transposed_data)

    def determinant(self) -> float:
        """Рекурсивное вычисление определителя"""
        rows, cols = self.shape
        if rows != cols:
            raise ValueError("Определитель существует только для квадратных матриц")

        # Базовые случаи
        if rows == 1:
            return self._values[0][0]
        if rows == 2:
            return self._values[0][0] * self._values[1][1] - self._values[0][1] * self._values[1][0]

        # Рекурсия (разложение по первой строке)
        det = 0.0
        for idx, element in enumerate(self._values[0]):
            # Вырезаем минор (подматрицу)
            sub_grid = [row[:idx] + row[idx + 1:] for row in self._values[1:]]

            # Знак чередуется: + - + -
            sign = 1 if idx % 2 == 0 else -1
            det += sign * element * Matrix(sub_grid).determinant()

        return det


if __name__ == "__main__":
    print("Тест ООП")
    m1 = Matrix([[1, 2], [2, 3]])
    m2 = Matrix([[2, 5], [7, 9]])

    print(f"Матрица 1:\n{m1}")
    print(f"Сложение:\n{m1 + m2}")
    print(f"Умножение матриц:\n{m1 * m2}")
    print(f"Транспонирование:\n{m1.transpose()}")
    print(f"Определитель m1: {m1.determinant()}")