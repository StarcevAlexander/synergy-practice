"""
Кейс-задача № 2.

Тестовая программа, демонстрирующая работу методов базового и
производного классов (наследование, переопределение, полиморфизм).

Предметная область — транспортные средства:
    Vehicle (базовый класс)
        ├── Car   (производный класс)
        └── Truck (производный класс)
"""

from __future__ import annotations


class Vehicle:
    """Базовый класс: общее поведение всех транспортных средств."""

    def __init__(self, brand: str, max_speed: int) -> None:
        self.brand = brand
        self.max_speed = max_speed

    def start(self) -> str:
        """Метод базового класса."""
        return f"{self.brand}: двигатель запущен."

    def describe(self) -> str:
        """Метод, который будет переопределён в производных классах."""
        return f"Транспортное средство {self.brand}, макс. скорость {self.max_speed} км/ч."


class Car(Vehicle):
    """Производный класс: легковой автомобиль."""

    def __init__(self, brand: str, max_speed: int, seats: int) -> None:
        super().__init__(brand, max_speed)  # вызов конструктора базового класса
        self.seats = seats

    def describe(self) -> str:
        """Переопределение метода базового класса + обращение к базовому через super()."""
        base = super().describe()
        return f"{base} Тип: легковой, мест: {self.seats}."

    def open_trunk(self) -> str:
        """Собственный метод производного класса."""
        return f"{self.brand}: багажник открыт."


class Truck(Vehicle):
    """Производный класс: грузовой автомобиль."""

    def __init__(self, brand: str, max_speed: int, capacity_t: float) -> None:
        super().__init__(brand, max_speed)
        self.capacity_t = capacity_t

    def describe(self) -> str:
        base = super().describe()
        return f"{base} Тип: грузовой, грузоподъёмность: {self.capacity_t} т."

    def load(self) -> str:
        return f"{self.brand}: груз размещён в кузове."


def demo() -> None:
    print("=== Демонстрация работы базового и производного классов ===\n")

    vehicles: list[Vehicle] = [
        Vehicle("Generic", 120),
        Car("Toyota", 180, seats=5),
        Truck("Volvo", 110, capacity_t=20.0),
    ]

    # Полиморфизм: один и тот же вызов describe() ведёт себя по-разному.
    for v in vehicles:
        print(f"[{type(v).__name__}]")
        print("  start():   ", v.start())          # унаследованный метод базового класса
        print("  describe():", v.describe())        # переопределённый метод
        # Методы, специфичные для производных классов:
        if isinstance(v, Car):
            print("  open_trunk():", v.open_trunk())
        if isinstance(v, Truck):
            print("  load():     ", v.load())
        print()


if __name__ == "__main__":
    demo()
