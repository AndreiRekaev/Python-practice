import calendar

class CalendarBookmark:
    """класс дескриптор - закладка для ежедневника"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if hasattr(instance, '_bookmark'):
            return instance._bookmark
        return 0

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0 or value >= len(instance):
            raise PageNotFoundError
        instance._bookmark = value



class CalendarBook(Book):
    
    bookmark = CalendarBookmark()
    
    """класс книги - ежедневник с закладкой"""
    def __init__(self, title, content=None):
        super().__init__(title, content)
        self._generate_calendar()

    def _generate_calendar(self):
        year = int(self.title)
        cl = calendar.TextCalendar(firstweekday=0)
        
        for month in range(1, 13):
            self._content.append(cl.formatmonth(year, month))

            for day in cl.itermonthdates(year, month):
                if day.month == month and day.year == year:
                    self._content.append(day.strftime("%Y-%m-%d"))

    def __len__(self):
        return len(self._content)

    def __getitem__(self, index):
        if index < 1 or index > len(self._content):
            raise PageNotFoundError
        return self._content[index - 1]

    def __setitem__(self, index, value):
        if isinstance(value, str):
            self._content[index - 1] = value
        else:
            raise TypeError
