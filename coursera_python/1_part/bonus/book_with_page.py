class Page:
    """класс страница"""

    def __init__(self, text=None, max_sign=2000):
        self._text = '' if text is None else text
        self.max_sign = max_sign
    
    def __len__(self):
        return len(self._text)

    def __str__(self):
        return self._text
    
    def __eq__(self, other):
        if isinstance(other, str):
            return len(self._text) == len(other)
        elif isinstance(other, Page):
            return len(self._text) == len(other._text)
        else:
            raise TypeError
    

    def __gt__(self, other):
        if isinstance(other, str):
            return len(self._text) > len(other)
        elif isinstance(other, Page):
            return len(self._text) > len(other._text)
        else:
            raise TypeError
    
    def __ge__(self, other):
        if isinstance(other, str):
            return len(self._text) >= len(other)
        elif isinstance(other, Page):
            return len(self._text) >= len(other._text)
        else:
            raise TypeError
    
    def __add__(self, other):
        if (len(self._text) + len(other) <= self.max_sign):
            if isinstance(other, str):
                self._text += other
            elif isinstance(other, Page):
                self._text += other._text
            else:
                raise TypeError
            return self
        else:
            raise TooLongTextError

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def __radd__(self, other):
        if isinstance(other, str):
            return other + self._text
        elif isinstance(other, Page):
            self.__add__(other)
            return self
        else:
            raise TypeError

class Book:
    """класс книга"""

    def __init__(self, title, content=None):
        self.title = title
        self._content = [] if content is None else content

    def __len__(self):
        return len(self._content)

    def __getitem__(self, index):
        if index < 1 or index > len(self._content):
            raise PageNotFoundError
        return self._content[index - 1]

    def __setitem__(self, index, value):
        if isinstance(value, str):
            self._content[index - 1]._text = value
        elif isinstance(value, Page):
            self._content[index - 1] = value
        else:
            raise TypeError
    
    def __str__(self):
        return self._content.__str__()
    
    def __ge__(self, other):
        return len(self._content) >= len(other._content)
    
    def __gt__(self, other):
        return len(self._content) >= len(other._content)

    def __eq__(self, other):
        if isinstance(other, Book):
            return len(self) == len(other) and all(p1 == p2 for p1, p2 in zip(self._content, other._content))
        raise TypeError
