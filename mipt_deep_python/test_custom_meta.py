import pytest
from custom_meta import CustomMeta


class TestCustomMeta:
    """Тесты для основного метакласса CustomMeta."""

    def test_class_attributes(self):
        """Тест атрибутов класса."""

        class CustomClass(metaclass=CustomMeta):
            x = 50
            y = 100

        assert CustomClass.custom_x == 50
        assert CustomClass.custom_y == 100

        with pytest.raises(AttributeError):
            _ = CustomClass.x
        with pytest.raises(AttributeError):
            _ = CustomClass.y

    def test_instance_attributes(self):
        """Тест атрибутов экземпляра."""

        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

        inst = CustomClass()

        assert inst.custom_x == 50
        assert inst.custom_val == 99

        with pytest.raises(AttributeError):
            _ = inst.x
        with pytest.raises(AttributeError):
            _ = inst.val

    def test_methods(self):
        """Тест методов."""

        class CustomClass(metaclass=CustomMeta):
            def line(self):
                return 100

            def another_method(self, x):
                return x * 2

        inst = CustomClass()

        assert inst.custom_line() == 100
        assert inst.custom_another_method(5) == 10

        with pytest.raises(AttributeError):
            inst.line()
        with pytest.raises(AttributeError):
            inst.another_method(5)

    def test_magic_methods(self):
        """Тест что магические методы не изменяются."""

        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def __str__(self):
                return "Custom_by_metaclass"

            def __repr__(self):
                return "CustomClass_instance"

        inst = CustomClass()

        assert str(inst) == "Custom_by_metaclass"
        assert repr(inst) == "CustomClass_instance"

        assert inst.custom_x == 50
        assert inst.custom_val == 99

    def test_dynamic_attributes(self):
        """Тест динамических атрибутов."""

        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

        inst = CustomClass()

        def add_dynamic_attributes(obj):
            obj.dynamic = "added later"
            obj.another_dynamic = 123

        add_dynamic_attributes(inst)

        assert inst.custom_dynamic == "added later"
        assert inst.custom_another_dynamic == 123

        with pytest.raises(AttributeError):
            _ = inst.dynamic
        with pytest.raises(AttributeError):
            _ = inst.another_dynamic

    def test_inheritance(self):
        """Тест наследования."""

        class BaseClass(metaclass=CustomMeta):
            base_attr = "base"

            def base_method(self):
                return "base_method"

        class DerivedClass(BaseClass):
            derived_attr = "derived"

            def derived_method(self):
                return "derived_method"

            def __init__(self):
                self.instance_attr = "instance"

        inst = DerivedClass()

        assert inst.custom_base_attr == "base"
        assert inst.custom_base_method() == "base_method"

        assert inst.custom_derived_attr == "derived"
        assert inst.custom_derived_method() == "derived_method"
        assert inst.custom_instance_attr == "instance"

        with pytest.raises(AttributeError):
            _ = inst.base_attr
        with pytest.raises(AttributeError):
            _ = inst.derived_attr
        with pytest.raises(AttributeError):
            _ = inst.instance_attr

    def test_multiple_instances(self):
        """Тест нескольких экземпляров."""

        class CustomClass(metaclass=CustomMeta):
            class_attr = "class_value"

            def __init__(self, value):
                self.instance_attr = value

        inst1 = CustomClass("value1")
        inst2 = CustomClass("value2")

        def setup_dynamic_attrs(inst1, inst2):
            inst1.dynamic1 = "dynamic1"
            inst2.dynamic2 = "dynamic2"

        setup_dynamic_attrs(inst1, inst2)

        assert inst1.custom_dynamic1 == "dynamic1"
        assert inst2.custom_dynamic2 == "dynamic2"

        with pytest.raises(AttributeError):
            _ = inst1.custom_dynamic2
        with pytest.raises(AttributeError):
            _ = inst2.custom_dynamic1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
