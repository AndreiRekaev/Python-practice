import os
import re
from collections import deque
from bs4 import BeautifulSoup
import unittest

def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""
    if start_page == end_page:
        return [start_page]

    # Очередь для BFS
    queue = deque()
    queue.append((start_page, [start_page]))  # (текущая страница, путь до неё)

    # Множество посещённых страниц
    visited = set()
    visited.add(start_page)

    while queue:
        current_page, path_to_current = queue.popleft()

        # Получаем все ссылки на текущей странице
        with open(os.path.join(path, current_page), encoding="utf-8") as file:
            content = file.read()
            links = re.findall(r"(?<=/wiki/)[\w()]+", content)

        for link in links:
            if link == end_page:
                return path_to_current + [link]

            if link not in visited and os.path.exists(os.path.join(path, link)):
                visited.add(link)
                queue.append((link, path_to_current + [link]))

    return []


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # Собираем статистику для каждой страницы
    statistic = {}
    for page in pages:
        statistic[page] = parse(os.path.join(path, page))

    return statistic

def get_imgs_count(body):
    imgs = len([
        img for img in body.find_all('img')
        if int(img.get('width', 0)) >= 200
    ])
    return imgs

def get_headers_count(body):
    headers = 0
    for header in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = header.get_text().strip()
        if text and text[0] in ['E', 'T', 'C']:
            headers += 1
    return headers

def get_links_len(body):
    linkslen = 0
    for tag in body.find_all('a'):
        # Получаем длину последовательности ссылок, начиная с текущей
        current_len = 1  # Учитываем текущую ссылку
        for sibling in tag.find_next_siblings():
            if sibling.name == 'a':
                current_len += 1
            else:
                break  # Прерываем, если встретился не ссылка
        if current_len > linkslen:
            linkslen = current_len
    return linkslen

def get_lists_count(body):
    lists = 0
    for list_tag in body.find_all(['ul', 'ol']):
        # Проверяем, что список не вложен в другой список
        if not list_tag.find_parent(['ul', 'ol']):
            lists += 1
    return lists


def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    with open(path_to_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    body_content = soup.find('div', id='bodyContent')

    imgs = get_imgs_count(body_content)
    headers = get_headers_count(body_content)
    linkslen = get_links_len(body_content)
    lists = get_lists_count(body_content)

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)

STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}

TESTCASES = (
    ('wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence', 'Python_(programming_language)']),

    ('wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3', 'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)

class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(result, {page: STATISTICS[page] for page in expected})

if __name__ == '__main__':
    unittest.main()