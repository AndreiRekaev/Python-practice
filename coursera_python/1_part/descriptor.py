
# Descriptor with amount comission mechanism

class Value:
    def __get__(self, obj, obj_type):
        return self.result

    def __set__(self, obj,
                value):
        self.result = value * (1 - obj.commission)
