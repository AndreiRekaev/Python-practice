from unittest.mock import Mock, call

import pytest
from process_json import process_json


class TestJsonProcessor:
    def test_basic_functionality(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 2

        calls = mock_callback.call_args_list
        assert calls[0][0] == ("key1", "WORD1")
        assert calls[1][0] == ("key1", "word2")

    def test_case_sensitivity_keys(self):
        json_str = '{"Key1": "value1", "key1": "value2"}'
        required_keys = ["Key1", "key1"]
        tokens = ["value1", "value2"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 2
        calls = mock_callback.call_args_list
        key_token_pairs = [(call[0][0], call[0][1]) for call in calls]

        assert ("Key1", "value1") in key_token_pairs
        assert ("key1", "value2") in key_token_pairs

    def test_case_insensitivity_tokens(self):
        """Тест регистронезависимости токенов"""
        json_str = '{"key1": "WORD1 Word2 wOrD3"}'
        required_keys = ["key1"]
        tokens = ["word1", "WORD2", "WoRd3"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 3

        calls = mock_callback.call_args_list
        found_tokens = [call[0][1] for call in calls]

        assert set(found_tokens) == {"word1", "WORD2", "WoRd3"}

    def test_multiple_spaces(self):
        json_str = '{"key1": "  word1   word2  word3  "}'
        required_keys = ["key1"]
        tokens = ["word1", "word2", "word3"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 3

        calls = mock_callback.call_args_list
        found_tokens = [call[0][1] for call in calls]

        assert set(found_tokens) == {"word1", "word2", "word3"}

    def test_key_not_found(self):
        json_str = '{"key1": "word1", "key3": "word3"}'
        required_keys = ["key2"]
        tokens = ["word1"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 0
        mock_callback.assert_not_called()

    def test_token_not_found(self):
        json_str = '{"key1": "word1 word2"}'
        required_keys = ["key1"]
        tokens = ["word3", "word4"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 0
        mock_callback.assert_not_called()

    def test_empty_parameters(self):
        json_str = '{"key1": "word1"}'

        mock_callback = Mock()
        process_json(json_str, [], ["word1"], mock_callback)
        assert mock_callback.call_count == 0

        mock_callback = Mock()
        process_json(json_str, ["key1"], [], mock_callback)
        assert mock_callback.call_count == 0
        mock_callback.assert_not_called()

        process_json(json_str, ["key1"], ["word1"], None)

    def test_invalid_json(self):
        invalid_json = '{"key1": "word1"'

        mock_callback = Mock()
        process_json(invalid_json, ["key1"], ["word1"], mock_callback)

        assert mock_callback.call_count == 0
        mock_callback.assert_not_called()

    def test_non_string_value(self):
        json_str = '{"key1": 123, "key2": ["word1", "word2"]}'
        required_keys = ["key1", "key2"]
        tokens = ["123", "word1"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 0
        mock_callback.assert_not_called()

    def test_exact_word_match(self):
        json_str = '{"key1": "word word1 word12"}'
        required_keys = ["key1"]
        tokens = ["word", "word1"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 2

        calls = mock_callback.call_args_list
        found_tokens = [call[0][1] for call in calls]

        assert "word" in found_tokens
        assert "word1" in found_tokens

    def test_stop_on_first_expected_key(self):
        json_str = '{"key1": "value1", "key2": "value2", "key3": "value3"}'
        required_keys = ["key1", "key3"]
        tokens = ["value1", "value2", "value3"]

        mock_callback = Mock()
        process_json(json_str, required_keys, tokens, mock_callback)

        calls = mock_callback.call_args_list
        processed_keys = [call[0][0] for call in calls]

        assert "key1" in processed_keys
        assert "key3" in processed_keys
        assert "key2" not in processed_keys

    def test_multiple_keys_multiple_tokens(self):
        json_str = (
            '{"name": "John Python Developer",'
            '"role": "Senior Python Engineer", "skills": "Java Python"}'
        )
        required_keys = ["name", "role", "skills"]
        tokens = ["Python", "Senior", "Java"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        assert mock_callback.call_count == 5

        expected_calls = [
            call("name", "Python"),
            call("role", "Python"),
            call("role", "Senior"),
            call("skills", "Python"),
            call("skills", "Java"),
        ]

        assert mock_callback.call_args_list == expected_calls


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
