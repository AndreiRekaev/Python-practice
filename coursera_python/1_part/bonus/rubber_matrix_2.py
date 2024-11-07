from itertools import chain

class Matrix:
    MAX_SIZE = 1000  
    def __init__(self, max_size=None):
        # вставьте вашу реализацию метода здесь
        self.size = 1
        self.max_size = max_size or Matrix.MAX_SIZE
        self.data = [[None] * self.size] * self.size

    def append(self, element=None):
        # вставьте вашу реализацию метода здесь
        if element is not None:
            if (self.size == self.max_size) and (self.data[-1][-1] is not None):
                raise IndexError
            combined_list = list(chain(*self.data))
            idx = combined_list.index(None)
            combined_list[idx] = element
            size = int(len(combined_list) ** 0.5)
                
            if (idx == size * (size - 1)) and (self.size < self.max_size):
                combined_list.extend([None, ] * ((size + 1) ** 2 - len(combined_list)))
                self.size = size + 1
                self.data = [combined_list[i:i + size + 1] for i in range(0, len(combined_list), size + 1)]
            else:
                self.data = [combined_list[i:i + size] for i in range(0, len(combined_list), size)]
            

    def pop(self):
        # вставьте вашу реализацию метода здесь
        if (self.size == 1):
            raise IndexError
        combined_list = list(chain(*self.data))
        idx = combined_list.index(None)
        element = combined_list[idx - 1]
        combined_list[idx - 1] = None
        if ((idx - 1) == (self.size - 1) ** 2 - (self.size - 1)):
            self.size -= 1
            combined_list = combined_list[:self.size ** 2]
            self.data = [combined_list[i:i + self.size] for i in range(0, len(combined_list), self.size)]
        else:
            self.data = [combined_list[i:i + self.size] for i in range(0, len(combined_list), self.size)]
        return element

    def __str__(self):
        # вставьте вашу реализацию метода здесь
        rows = []
        for i in range(self.size):
            row = [x if x is not None else 'None' for x in self.data[i]]
            rows.append(' '.join(map(str, row)))
        
        return '\n'.join(rows)

    @classmethod
    def from_iter(cls, iter_obj, max_size=None):
        # вставьте вашу реализацию метода здесь
        if not hasattr(iter_obj, '__iter__'):
            raise TypeError
        else:
            size = max_size
            matrix = cls(max_size=size)
            for i in iter_obj:
                if i is not None:
                    matrix.append(i)
        return matrix
