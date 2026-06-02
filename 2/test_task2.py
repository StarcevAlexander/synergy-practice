"""Тесты к кейс-задаче № 2."""

from task2 import Vehicle, Car, Truck


def test_inheritance():
    car = Car("Toyota", 180, seats=5)
    # Унаследованный метод базового класса
    assert car.start() == "Toyota: двигатель запущен."
    # Производный класс — экземпляр и базового типа
    assert isinstance(car, Vehicle)


def test_method_override():
    base = Vehicle("Generic", 120)
    car = Car("Toyota", 180, seats=5)
    truck = Truck("Volvo", 110, capacity_t=20.0)

    # describe() ведёт себя по-разному (полиморфизм)
    assert "Транспортное средство" in base.describe()
    assert "легковой" in car.describe()
    assert "грузовой" in truck.describe()
    # super() в производном классе подтягивает текст базового метода:
    # describe() автомобиля начинается с базового описания этого же объекта.
    assert car.describe().startswith(Vehicle.describe(car))


def test_own_methods():
    assert Car("Kia", 170, 4).open_trunk() == "Kia: багажник открыт."
    assert Truck("MAN", 100, 15).load() == "MAN: груз размещён в кузове."


if __name__ == "__main__":
    test_inheritance()
    test_method_override()
    test_own_methods()
    print("Все тесты пройдены успешно.")
