from custom_list import CustomList


class TestCustomList:
    def test_creation(self):
        cl = CustomList([1, 2, 3])
        assert list(cl) == [1, 2, 3]
        assert isinstance(cl, CustomList)
        assert isinstance(cl, list)

    def test_addition_custom_lists(self):
        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([1, 2, 7])
        result = cl1 + cl2

        assert isinstance(result, CustomList)
        assert list(result) == [6, 3, 10, 7]
        assert list(cl1) == [5, 1, 3, 7]
        assert list(cl2) == [1, 2, 7]

    def test_addition_with_list(self):
        cl = CustomList([10])
        lst = [2, 5]

        result1 = cl + lst
        result2 = lst + cl

        assert isinstance(result1, CustomList)
        assert isinstance(result2, CustomList)
        assert list(result1) == [12, 5]
        assert list(result2) == [12, 5]

    def test_addition_with_number(self):
        cl = CustomList([2, 5])

        result1 = cl + 10
        result2 = 10 + cl

        assert isinstance(result1, CustomList)
        assert isinstance(result2, CustomList)
        assert list(result1) == [12, 15]
        assert list(result2) == [12, 15]

    def test_subtraction_custom_lists(self):
        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([1, 2, 7])
        result = cl1 - cl2

        assert isinstance(result, CustomList)
        assert list(result) == [4, -1, -4, 7]
        assert list(cl1) == [5, 1, 3, 7]
        assert list(cl2) == [1, 2, 7]

    def test_subtraction_with_list(self):
        cl = CustomList([10])
        lst = [2, 5]

        result1 = cl - lst
        result2 = lst - cl

        assert isinstance(result1, CustomList)
        assert isinstance(result2, CustomList)
        assert list(result1) == [8, -5]
        assert list(result2) == [-8, 5]

    def test_subtraction_with_number(self):
        cl = CustomList([2, 5])

        result1 = cl - 10
        result2 = 10 - cl

        assert isinstance(result1, CustomList)
        assert isinstance(result2, CustomList)
        assert list(result1) == [-8, -5]
        assert list(result2) == [8, 5]

    def test_different_lengths(self):
        cl1 = CustomList([1, 2])
        cl2 = CustomList([1, 2, 3, 4])

        result_add = cl1 + cl2
        result_sub = cl1 - cl2

        assert list(result_add) == [2, 4, 3, 4]
        assert list(result_sub) == [0, 0, -3, -4]

    def test_comparison_operations(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([4, 5])
        cl3 = CustomList([1, 2, 3])

        assert cl1 != cl2
        assert cl1 == cl3
        assert cl1 < cl2
        assert cl2 > cl1
        assert cl1 <= cl3
        assert cl2 >= cl1
        assert not cl1 > cl2
        assert not cl2 < cl1

    def test_str_representation(self):
        cl = CustomList([1, 2, 3])
        result = str(cl)

        assert "1, 2, 3" in result
        assert "sum = 6" in result

    def test_inplace_operations(self):
        cl = CustomList([1, 2, 3])
        cl += CustomList([4, 5])

        assert isinstance(cl, CustomList)
        assert list(cl) == [5, 7, 3]

        cl -= [1, 1]
        assert list(cl) == [4, 6, 3]

    def test_empty_lists(self):
        cl1 = CustomList([])
        cl2 = CustomList([1, 2])

        result_add = cl1 + cl2
        result_sub = cl1 - cl2

        assert list(result_add) == [1, 2]
        assert list(result_sub) == [-1, -2]

    def test_single_element(self):
        cl = CustomList([5])

        result_add = cl + 3
        result_sub = cl - 3

        assert list(result_add) == [8]
        assert list(result_sub) == [2]

    def test_negative_numbers(self):
        cl1 = CustomList([-1, -2, -3])
        cl2 = CustomList([1, 2])

        result_add = cl1 + cl2
        result_sub = cl1 - cl2

        assert list(result_add) == [0, 0, -3]
        assert list(result_sub) == [-2, -4, -3]

    def test_preserve_original(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([4, 5])

        original_cl1 = list(cl1)
        original_cl2 = list(cl2)

        _ = cl1 + cl2
        _ = cl1 - cl2

        assert list(cl1) == original_cl1
        assert list(cl2) == original_cl2

    def test_comparison_with_different_sums(self):
        cl1 = CustomList([10])
        cl2 = CustomList([1, 2, 3])
        cl3 = CustomList([4, 5, 1])

        assert cl1 > cl2
        assert cl2 < cl1
        assert cl1 == cl3
        assert cl1 >= cl3
        assert cl1 <= cl3
