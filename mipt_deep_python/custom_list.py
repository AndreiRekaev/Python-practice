class CustomList(list):
    def _operate(self, other, operation, reverse=False):
        if isinstance(other, (int, float)):
            result = CustomList(
                operation(other, x) if reverse else operation(x, other)
                for x in self
            )
        else:
            if isinstance(other, list):
                other = CustomList(other)

            max_len = max(len(self), len(other))
            result = CustomList()

            for i in range(max_len):
                left = self[i] if i < len(self) else 0
                right = other[i] if i < len(other) else 0

                if reverse:
                    result.append(operation(right, left))
                else:
                    result.append(operation(left, right))

        return result

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self._operate(other, lambda x, y: x + y, reverse=True)

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)

    def __rsub__(self, other):
        return self._operate(other, lambda x, y: x - y, reverse=True)

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        return NotImplemented

    def __str__(self):
        elements = ", ".join(str(x) for x in self)
        return f"[{elements}] sum = {sum(self)}"

    def __iadd__(self, other):
        result = self + other
        self.clear()
        self.extend(result)
        return self

    def __isub__(self, other):
        result = self - other
        self.clear()
        self.extend(result)
        return self
