import os
import tempfile

import pytest
from file_filter_generator import filter_lines


class TestFileFilterGenerator:
    def create_test_file(self, content: str) -> str:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            suffix=".txt",
        ) as f:
            f.write(content)
            return f.name

    def test_basic_functionality(self):
        content = """а Роза упала на лапу Азора
                    красная роза цветет в саду
                    солнце светит ярко
                    зима близко"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза"], ["азора"]))
            assert results == ["красная роза цветет в саду"]

            results = list(filter_lines(file_path, ["роза"], []))
            assert results == [
                "а Роза упала на лапу Азора",
                "красная роза цветет в саду",
            ]

        finally:
            os.unlink(file_path)

    def test_case_insensitivity(self):
        """Тест нечувствительности к регистру"""
        content = """РОЗА красная
                    Азора прекрасна
                    роза упала"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза"], ["азора"]))
            assert results == ["РОЗА красная", "роза упала"]

        finally:
            os.unlink(file_path)

    def test_stop_words_priority(self):
        content = """роза и азора вместе
                    только роза
                    только азора
                    ничего нет"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза"], ["азора"]))
            assert results == ["только роза"]

        finally:
            os.unlink(file_path)

    def test_multiple_search_words(self):
        content = """красная роза
                    белая лилия
                    желтый тюльпан
                    розовый пион"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза", "лилия"], []))
            assert results == ["красная роза", "белая лилия"]

        finally:
            os.unlink(file_path)

    def test_exact_word_match(self):
        content = """роза прекрасна
                    розы цветут
                    розан пышный
                    розовый цвет"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза"], []))
            assert results == ["роза прекрасна"]

            results = list(filter_lines(file_path, ["розы"], []))
            assert results == ["розы цветут"]

        finally:
            os.unlink(file_path)

    def test_empty_file(self):
        file_path = self.create_test_file("")

        try:
            results = list(filter_lines(file_path, ["роза"], []))
            assert not results

        finally:
            os.unlink(file_path)

    def test_file_object_input(self):
        content = """роза красная
                     лилия белая"""

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
        ) as f:
            f.write(content)
            file_path = f.name

        try:
            with open(file_path, "r", encoding="utf-8") as file_obj:
                results = list(filter_lines(file_obj, ["роза"], []))
                assert results == ["роза красная"]

        finally:
            os.unlink(file_path)

    def test_large_file_simulation(self):
        content = "\n".join(
            [
                f"строка {i} роза" if i % 100 == 0 else f"строка {i}"
                for i in range(1000)
            ],
        )

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза"], []))
            assert (
                len(results) == 10
            )  # 1000 / 100 = 10 строк со словом "роза"

        finally:
            os.unlink(file_path)

    def test_multiple_matches_in_line(self):
        content = """роза и лилия красивые цветы
                     тюльпан цветет весной"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, ["роза", "лилия"], []))
            assert results == [
                "роза и лилия красивые цветы",
            ]

        finally:
            os.unlink(file_path)

    def test_empty_search_words(self):
        content = """роза красная
                     лилия белая"""

        file_path = self.create_test_file(content)

        try:
            results = list(filter_lines(file_path, [], ["роза"]))
            assert not results

        finally:
            os.unlink(file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
