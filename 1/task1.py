"""
Кейс-задача № 1.

Дан одномерный массив A размерности N. Найти сумму отрицательных
элементов, расположенных МЕЖДУ максимальным и минимальным элементами.

Идея решения:
1. Находим индексы максимального (i_max) и минимального (i_min) элементов.
2. Определяем границы интервала "между" ними — это индексы строго
   между min(i_max, i_min) и max(i_max, i_min) (сами max и min не входят).
3. Суммируем те элементы интервала, которые отрицательны.

Если максимум и минимум стоят рядом (или это один и тот же элемент),
между ними элементов нет — сумма равна 0.
"""

from typing import List


def sum_negatives_between_extremes(a: List[float]) -> float:
    """Возвращает сумму отрицательных элементов между макс. и мин. элементами."""
    if len(a) < 3:
        # Чтобы существовал хотя бы один элемент "между", нужно минимум 3 элемента.
        return 0.0

    i_max = max(range(len(a)), key=lambda i: a[i])
    i_min = min(range(len(a)), key=lambda i: a[i])

    left = min(i_max, i_min)
    right = max(i_max, i_min)

    # Срез (left, right) — строго между крайними элементами.
    return sum(x for x in a[left + 1:right] if x < 0)


def read_array_from_input() -> List[float]:
    """Считывает массив из стандартного ввода (числа через пробел)."""
    n = int(input("Введите размерность N: ").strip())
    print(f"Введите {n} элементов через пробел:")
    values = list(map(float, input().split()))
    if len(values) != n:
        raise ValueError(f"Ожидалось {n} элементов, получено {len(values)}.")
    return values


def main() -> None:
    a = read_array_from_input()
    result = sum_negatives_between_extremes(a)
    print(f"Массив: {a}")
    print(f"Сумма отрицательных элементов между макс. и мин.: {result}")


if __name__ == "__main__":
    main()
