# First of all, we don't save any other elements in the dictionary
import unittest  # Module for tests


def add_ingot(purse: dict[str, int]) -> dict[str, int]:
    answer: dict[str, int] = {}

    if ("gold_ingots" not in purse) or (purse["gold_ingots"] + 1 < 0):
        answer["gold_ingots"] = 1
    else:
        answer["gold_ingots"] = purse["gold_ingots"] + 1

    return answer


def get_ingot(purse: dict[str, int]) -> dict[str, int]:
    answer: dict[str, int] = {}

    if ("gold_ingots" in purse) and (purse["gold_ingots"] > 1):
        answer["gold_ingots"] = purse["gold_ingots"] - 1

    return answer


def empty(purse: dict[str, int]) -> dict[str, int]:
    answer: dict[str, int] = {}

    return answer


if __name__ == "__main__":  # Case if we don't import module (tests)
    class TestsEx00(unittest.TestCase):

        def tests_add_ingot(self):
            self.assertEqual(add_ingot({}), {"gold_ingots": 1})
            self.assertEqual(add_ingot({"something": 1}), {"gold_ingots": 1})
            self.assertEqual(add_ingot({"gold_ingots": 0}), {"gold_ingots": 1})
            self.assertEqual(add_ingot({"gold_ingots": 1}), {"gold_ingots": 2})
            self.assertEqual(add_ingot({"gold_ingots": -3}), {"gold_ingots": 1})
            self.assertEqual(add_ingot(add_ingot({"gold_ingots": 1})), {"gold_ingots": 3})
            self.assertEqual(add_ingot(add_ingot({"gold_ingots": -3})), {"gold_ingots": 2})

        def tests_get_ingot(self):
            self.assertEqual(get_ingot({}), {})
            self.assertEqual(get_ingot({"something": 1}), {})
            self.assertEqual(get_ingot({"gold_ingots": 1}), {})
            self.assertEqual(get_ingot({"gold_ingots": -2}), {})
            self.assertEqual(get_ingot({"gold_ingots": 20}), {"gold_ingots": 19})

        def tests_empty(self):
            self.assertEqual(empty({}), {})
            self.assertEqual(empty({"gold_ingots": 1}), {})
            self.assertEqual(empty({"something": -2}), {})
            self.assertEqual(empty({"gold_ingots": -2}), {})
            self.assertEqual(empty({"gold_ingots": 20}), {})

        def tests_combinations(self):
            self.assertEqual(empty(empty(empty({}))), {})
            self.assertEqual(add_ingot(add_ingot(add_ingot({}))), {"gold_ingots": 3})
            self.assertEqual(get_ingot(get_ingot(get_ingot({"gold_ingots": 5}))), {"gold_ingots": 2})
            self.assertEqual(get_ingot(add_ingot(get_ingot({"gold_ingots": 5}))), {"gold_ingots": 4})
            self.assertEqual(add_ingot(get_ingot(add_ingot(empty({"gold_ingots": 1})))), {"gold_ingots": 1})

    unittest.main()
