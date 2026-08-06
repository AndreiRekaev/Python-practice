import pytest
from descriptors import (
    Currency,
    Integer,
    String,
)


class TestBaseDescriptors:
    """Тесты базовых дескрипторов."""

    def test_integer_descriptor(self):
        """Тест дескриптора для целых чисел."""

        class TestClass:
            value = Integer()

        obj = TestClass()

        obj.value = 42
        assert obj.value == 42

        obj.value = 0
        assert obj.value == 0

        obj.value = -100
        assert obj.value == -100

        with pytest.raises(TypeError):
            obj.value = "not a number"

        with pytest.raises(TypeError):
            obj.value = 3.14

    def test_string_descriptor(self):
        """Тест дескриптора для строк."""

        class TestClass:
            name = String(min_length=2, max_length=5)

        obj = TestClass()

        obj.name = "ab"
        assert obj.name == "ab"

        obj.name = "abcde"
        assert obj.name == "abcde"

        with pytest.raises(TypeError):
            obj.name = 123

        with pytest.raises(ValueError):
            obj.name = "a"

        with pytest.raises(ValueError):
            obj.name = "abcdef"

    def test_currency_descriptor(self):
        """Тест дескриптора для валют."""

        class TestClass:
            curr = Currency()

        obj = TestClass()

        obj.curr = "USD"
        assert obj.curr == "USD"

        obj.curr = "EUR"
        assert obj.curr == "EUR"

        obj.curr = "RUB"
        assert obj.curr == "RUB"

        with pytest.raises(ValueError):
            obj.curr = "US"

        with pytest.raises(ValueError):
            obj.curr = "USDD"

        with pytest.raises(ValueError):
            obj.curr = "usd"

        with pytest.raises(ValueError):
            obj.curr = "U1D"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
