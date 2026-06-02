"""Тесты к кейс-задаче № 1. Запуск: python -m pytest test_task1.py  (или python test_task1.py)."""

from task1 import sum_negatives_between_extremes


def run_tests() -> None:
    # max=9 (индекс 1), min=-7 (индекс 5). Между ними индексы 2..4: -3, 4, -1 -> -4
    assert sum_negatives_between_extremes([1, 9, -3, 4, -1, -7, 2]) == -4

    # Между крайними нет отрицательных
    assert sum_negatives_between_extremes([5, 1, 2, 3, -1]) == 0

    # max и min рядом — между ними пусто
    assert sum_negatives_between_extremes([10, -10, 5]) == 0

    # Слишком короткий массив
    assert sum_negatives_between_extremes([1, 2]) == 0
    assert sum_negatives_between_extremes([]) == 0

    # min слева, max справа: [-8, -2, -3, 7]; между индексами 0 и 3: -2, -3 -> -5
    assert sum_negatives_between_extremes([-8, -2, -3, 7]) == -5

    print("Все тесты пройдены успешно.")


# pytest подхватит эти функции как тесты
def test_basic():
    assert sum_negatives_between_extremes([1, 9, -3, 4, -1, -7, 2]) == -4


def test_no_negatives():
    assert sum_negatives_between_extremes([5, 1, 2, 3, -1]) == 0


if __name__ == "__main__":
    run_tests()
