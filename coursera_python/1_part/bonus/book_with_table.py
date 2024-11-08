class AdvancedPerson(Person):
    def search(self, book, name_page):
        """возвращает номер страницы name_page из книги book"""
        return book.search(name_page)

    def read(self, book, page):
        # переопределите метод
        if isinstance(page, str):
            page = book.search(page)
        return book.read(page)

    def write(self, book, page, text):
        # переопределите метод
        if isinstance(page, str):
            page = book.search(page)
        return book.write(page, text)
           
        
class NovelWithTable(Novel):
    """класс - книга с оглавлением"""

    def __init__(self, author, year, title, content=None, table=None):
        # переопределите метод
        self.table = table or {}
        super().__init__(author, year, title, content)
        

    def search(self, name_page):
        # напишите вашу реализацию метода здесь
        if name_page in self.table:
            return self.table[name_page]
        raise PageNotFoundError

    def add_chapter(self, chapter, page):
        # напишите вашу реализацию метода здесь
        self.table[chapter] = page

    def remove_chapter(self, chapter):
        # напишите вашу реализацию метода здесь
        if chapter in self.table:
            del self.table[chapter]
