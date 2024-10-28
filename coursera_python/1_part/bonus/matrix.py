"""
Резиновая матрица.

Вы с друзьями пишете программу для работы с двумерными матрицами. Часть функционала, необходимого для нормальной работы программы, поручено написать вам. А именно:
- функцию для создания "пустой" матрицы размером: size x size, заполненной "нулевыми" элементами (None)
- функция для добавления элемента в матрицу с возможностью расширения самой матрицы
- функция преобразования матрицы в строковое представление

Правила добавления элементов к матрице:
- матрица заполняется построчно, слева-направо, с первой строки до последней
- добавляемый элемент занимает позицию первого свободного "нулевого" элемента
- добавление "нулевого" элемента (None) игнорируется
- в случае, когда добавляемый элемент, занимает место первого элемента в последней строке матрицы, матрицу необходимо "расширить", увеличив размер матрицы на 1 (добавить один столбец и одну строку), при этом добавленные в матрицу элементы сдвигаются к началу таким образом, чтобы между ними не было "нулевых" элементов.

У вас уже есть готовый шаблон кода с названиями функций и описанием их работы:

def create_matrix(size):
    """
    Функция принимает на вход размер квадратной матрицы. Возвращает 'пустую' матрицу
    размером size x size, (все элементы матрицы имеют значение равное None).
    :param size: int > 0
    :return: list 
    """
   # вставьте вашу реализацию функции здесь
 
def add_element(element, matrix):
    """
    Функция добавляет element в матрицу matrix и при необходимости изменяет размер
    матрицы. Возвращает полученную матрицу.
    :param element: string
    :param matrix: list
    :return: list
    """
   # вставьте вашу реализацию функции здесь
 
def matrix_to_string(matrix):
    """
    Функция создает строковое представление matrix - строку, в которой строки матрицы 
    разделены переносом строки, а элементы строки разделены пробелами.
    :param matrix: list
    :return: string
    """
    # вставьте вашу реализацию функции здесь
Используя шаблон, напишите реализации функций. Вы может добавить объявления дополнительных функций, если они необходимы для вашего решения.
Пример работы функций:

>>> from matrix import *
>>> matrix = create_matrix(2)
>>> print(matrix_to_string(matrix))
None None
None None
>>> matrix = add_element(5, matrix)
>>> matrix = add_element(7, matrix)
>>> print(matrix_to_string(matrix))
5 7
None None
>>> matrix = add_element(9, matrix)
>>> print(matrix_to_string(matrix))
5 7 9
None None None
None None None
 Примечание: в решении запрещено использовать сторонние библиотеки (например: numpy)
"""


from itertools import chain

def create_matrix(size):    
    """
    Функция принимает на вход размер квадратной матрицы. Возвращает 'пустую' матрицу
    размером size x size, (все элементы матрицы имеют значение равное None).
    :param size: int
    :return: list
    """
    return [[None for _ in range(size)] for _ in range(size)]


def add_element(element, matrix):
    """
    Функция добавляет element в матрицу matrix и при необходимости изменяет размер
    матрицы. Возвращает полученную матрицу.
    :param element: string
    :param matrix: list
    :return: list
    """
    if element is not None:
        rows, cols = len(matrix), len(matrix[0])
        for row in range(rows):
            for col in range(cols):
                if (matrix[row][col] is None) and (row < rows - 1):
                    matrix[row][col] = element
                    return matrix

        # Создаем новую матрицу, увеличивая ее размер на 1 строку и 1 столбец

        new_matrix = [[None] * (cols + 1) for _ in range(rows + 1)]
        combined_list = list(chain(*matrix))
        index = 0
        # Копируем данные из исходной матрицы в новую
        for row in range(rows + 1):
            for col in range(cols + 1):
                if combined_list[index] is not None:
                    new_matrix[row][col] = combined_list[index]
                    index += 1
                else:
                    break


        i, j = next(((i, j) for i, row in enumerate(new_matrix) for j, elem in enumerate(row) if elem is None), None)
        new_matrix[i][j] = element

        return new_matrix
    else:
        return matrix


def matrix_to_string(matrix):
    """
    Функция создает строковое представление matrix
    :param matrix: list
    :return: string
    """
    return '\n'.join([' '.join(map(str, row)) for row in matrix])
