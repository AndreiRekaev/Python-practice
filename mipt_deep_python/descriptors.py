from abc import ABC, abstractmethod


class BaseDescriptor(ABC):
    """Базовый класс дескриптора с проверкой данных."""

    def __init__(self):
        self.private_name = None

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        self._validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def _validate(self, value):
        """Абстрактный метод для проверки значения."""


class Integer(BaseDescriptor):
    """Дескриптор для целых чисел."""

    def _validate(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f"Ожидается целое число, получен {type(value).__name__}",
            )


class String(BaseDescriptor):
    """Дескриптор для строк."""

    def __init__(self, min_length=0, max_length=255):
        self.min_length = min_length
        self.max_length = max_length

    def _validate(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"Ожидается строка, получен {type(value).__name__}",
            )

        if len(value) < self.min_length:
            raise ValueError(
                f"Длина строки должна быть не менее {self.min_length} символов",
            )

        if len(value) > self.max_length:
            raise ValueError(
                f"Длина строки должна быть не более {self.max_length} символов",
            )


class Currency(String):
    """Дескриптор для валютных кодов (например, USD, EUR, RUB)."""

    def __init__(self):
        super().__init__(min_length=3, max_length=3)

    def _validate(self, value):
        super()._validate(value)
        if not value.isalpha() or not value.isupper():
            raise ValueError("Код валюты должен состоять из 3 заглавных букв")
