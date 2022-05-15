import logging

# Example 1
logging.basicConfig(level=logging.WARNING)

def hypotenuse(a, b):
    """Compute the hypotenuse"""
    return (a**2 + b**2)**0.5

kwargs = {'a':3, 'b':4, 'c':hypotenuse(3, 4)}

logging.debug("a = {a}, b = {b}".format(**kwargs))
logging.info("Hypotenuse of {a}, {b} is {c}".format(**kwargs))
logging.warning("a={a} and b={b} are equal".format(**kwargs))
logging.error("a={a} and b={b} cannot be negative".format(**kwargs))
logging.critical("Hypotenuse of {a}, {b} is {c}".format(**kwargs))

# Example 2

class FirstClass:
    def __init__(self):
        self.current_number = 0

        # Создаем Logger

    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)

# Создаем обработчик для записи данных в файл
    logger_handler = logging.FileHandler('python_logging.log')
    logger_handler.setLevel(logging.INFO)

# Создаем Formatter для форматирования сообщений в логе
    logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Добавляем Formatter в обработчик
    logger_handler.setFormatter(logger_formatter)

# Добавляем обработчик в Logger
    self.logger.addHandler(logger_handler)
    self.logger.info('Настройка логгирования окончена!')


    def increment_number(self):
        self.current_number += 1


    self.logger.warning('Число увеличивается!')
    self.logger.info('Число еще увеличивается!!')


    def decrement_number(self):
        self.current_number -= 1


    def clear_number(self):
        self.current_number = 0


    self.logger.warning('Очистка значения!')
    self.logger.info('Значение еще не очищено!!')
