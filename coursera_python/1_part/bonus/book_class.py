class Book:
    def __init__(self, title, content=None):
        self.title = title
        self.content = content or []
        self.size = len(self.content)

    def read(self, page):
        raise NotImplementedError

    def write(self, page, text):
        raise NotImplementedError


class Novel(Book):
    """класс описывающий книгу и методы работы с ней"""

    def __init__(self, author, year, title, content=None):
        """конструктор"""
        self.author = author
        self.year = year
        self.bookmark = dict()
        super().__init__(title, content)
        
    def read(self, page):
        """возвращает страницу"""
        if page < 0 or page > self.size:
            raise PageNotFoundError
        return self.content[page]

    def set_bookmark(self, person, page):
        """устанавливает закладку в книгу book"""
        self.bookmark[person] = page

    def get_bookmark(self, person):
        """получает номер страницы установленной закладки в книге book"""
        if person not in self.bookmark:
            raise PageNotFoundError
        return self.bookmark[person]

    def del_bookmark(self, person):
        """удаляет закладку читателя person, если она установлена"""
        if person in self.bookmark:
            del self.bookmark[person]

    def write(self, page, text):
        """делает запись текста text на страницу page """
        raise PermissionDeniedError


class Notebook(Book):
    """класс описывающий тетрадь и методы работы с ней"""

    def __init__(self, title, size=12, max_sign=2000, content=None):
        """конструктор"""
        self.max_sign = max_sign
        super().__init__(title, content or ['' for _ in range(size)])

    def read(self, page):
        """возвращает страницу с номером page"""
        if page < 0 or page > self.size:
            raise PageNotFoundError
        return self.content[page]
        

    def write(self, page, text):
        """делает запись текста text на страницу с номером page """
        if len(text) + len(self.read(page)) > self.max_sign:
            raise TooLongTextError
        if page < 0 or page > self.size:
            raise PageNotFoundError
        self.content[page] += text


class Person:
    """класс описывающий человека и методы работы с книгой"""

    def __init__(self, name):
        """конструктор"""
        self.name = name

    def read(self, book, page):
        """читаем страницу с номером page в книге book"""
        return book.read(page)

    def write(self, book, page, text):
        """пишем на страницу с номером page в книге book"""
        book.write(page, text)

    def set_bookmark(self, book, page):
        """устанавливаем закладку в книгу book на страницу с номером page"""
        if not isinstance(book, Novel):
            raise NotExistingExtensionError
        book.set_bookmark(self, page)
            

    def get_bookmark(self, book):
        """получаем номер страницы установленной закладки в книге book"""
        if not isinstance(book, Novel):
            raise NotExistingExtensionError
        return book.get_bookmark(self)

    def del_bookmark(self, book):
        """удаляет закладку из книги book"""
        if not isinstance(book, Novel):
            raise NotExistingExtensionError
        book.del_bookmark(self)
