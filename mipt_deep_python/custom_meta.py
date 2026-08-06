class CustomMeta(type):
    def __new__(mcs, name, bases, classdict):
        new_classdict = {}

        for attr_name, attr_value in classdict.items():
            if attr_name.startswith("__") and attr_name.endswith("__"):
                new_classdict[attr_name] = attr_value
            else:
                new_attr_name = f"custom_{attr_name}"
                new_classdict[new_attr_name] = attr_value

        new_class = super().__new__(mcs, name, bases, new_classdict)

        def custom_setattr(instance, name, value):
            if not (name.startswith("__") and name.endswith("__")):
                name = f"custom_{name}"
            object.__setattr__(instance, name, value)

        new_class.__setattr__ = custom_setattr

        def custom_getattribute(instance, name):
            if not (
                name.startswith("__") and name.endswith("__")
            ) and not name.startswith("custom_"):
                raise AttributeError(
                    f"'{instance.__class__.__name__}'"
                    f"object has no attribute '{name}'",
                )

            return object.__getattribute__(instance, name)

        new_class.__getattribute__ = custom_getattribute

        return new_class
