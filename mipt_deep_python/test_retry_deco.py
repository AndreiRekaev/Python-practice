import sys
from io import StringIO

import pytest
from retry_deco import retry_deco


class TestRetryDecorator:
    def capture_output(self, func, *args, **kwargs):
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        result = None
        exception_raised = None

        try:
            result = func(*args, **kwargs)
        except (ValueError, RuntimeError, TypeError) as e:
            exception_raised = e
        finally:
            sys.stdout = old_stdout
            output = captured_output.getvalue()

        return result, exception_raised, output

    def test_successful_execution(self):
        @retry_deco(3)
        def add(a, b):
            return a + b

        result, exception, output = self.capture_output(add, 4, 2)

        assert result == 6
        assert exception is None

        expected_lines = [
            'run "add" with positional args = (4, 2)',
            'run "add" with positional args = (4, 2), attempt = 1, '
            "result = 6",
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == expected_lines[0]
        assert lines[1] == expected_lines[1]

    def test_keyword_arguments(self):
        @retry_deco(3)
        def add(a, b):
            return a + b

        result, exception, output = self.capture_output(add, 4, b=3)

        assert result == 7
        assert exception is None

        expected_lines = [
            (
                'run "add" with positional args = (4,), '
                "keyword kwargs = {'b': 3}"
            ),
            (
                'run "add" with positional args = (4,), '
                "keyword kwargs = {'b': 3}, attempt = 1, result = 7"
            ),
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == expected_lines[0]
        assert lines[1] == expected_lines[1]

    def test_retry_on_exception(self):
        call_count = 0

        @retry_deco(2)
        def failing_function():
            nonlocal call_count
            call_count += 1
            raise RuntimeError("Test error")

        result, exception, output = self.capture_output(failing_function)

        assert result is None
        assert isinstance(exception, RuntimeError)
        assert call_count == 3

        expected_lines = [
            'run "failing_function" with ',
            (
                'run "failing_function" with , attempt = 1, '
                "exception = RuntimeError"
            ),
            (
                'run "failing_function" with , attempt = 2, '
                "exception = RuntimeError"
            ),
            (
                'run "failing_function" with , attempt = 3, '
                "exception = RuntimeError"
            ),
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 4
        for i, line in enumerate(lines):
            assert expected_lines[i] in line

    def test_expected_exception_no_retry(self):
        call_count = 0

        @retry_deco(3, [ValueError])
        def function_with_expected_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Expected error")

        result, exception, output = self.capture_output(
            function_with_expected_error,
        )

        assert result is None
        assert isinstance(exception, ValueError)
        assert call_count == 1

        expected_lines = [
            'run "function_with_expected_error" with ',
            (
                'run "function_with_expected_error" with , attempt = 1, '
                "exception = ValueError"
            ),
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 2
        for i, line in enumerate(lines):
            assert expected_lines[i] in line

    def test_mixed_exceptions(self):
        call_count = 0

        @retry_deco(2, [ValueError])
        def mixed_exceptions():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("Unexpected error")
            if call_count == 2:
                raise ValueError("Expected error")
            return "success"

        result, exception, output = self.capture_output(mixed_exceptions)

        assert result is None
        assert isinstance(exception, ValueError)
        assert call_count == 2

        expected_lines = [
            'run "mixed_exceptions" with ',
            (
                'run "mixed_exceptions" with , attempt = 1, '
                "exception = RuntimeError"
            ),
            (
                'run "mixed_exceptions" with , attempt = 2, '
                "exception = ValueError"
            ),
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 3
        for i, line in enumerate(lines):
            assert expected_lines[i] in line

    def test_success_after_retry(self):
        call_count = 0

        @retry_deco(3)
        def succeeds_after_failures():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("Temporary failure")
            return "success"

        result, exception, output = self.capture_output(
            succeeds_after_failures,
        )

        assert result == "success"
        assert exception is None
        assert call_count == 3

        expected_lines = [
            'run "succeeds_after_failures" with ',
            (
                'run "succeeds_after_failures" with , attempt = 1, '
                "exception = RuntimeError"
            ),
            (
                'run "succeeds_after_failures" with , attempt = 2, '
                "exception = RuntimeError"
            ),
            (
                'run "succeeds_after_failures" with , attempt = 3, '
                "result = success"
            ),
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 4
        for i, line in enumerate(lines):
            assert expected_lines[i] in line

    def test_no_args_function(self):
        @retry_deco(2)
        def no_args():
            return "result"

        result, exception, output = self.capture_output(no_args)

        assert result == "result"
        assert exception is None

        expected_lines = [
            'run "no_args" with ',
            'run "no_args" with , attempt = 1, result = result',
        ]

        lines = output.strip().split("\n")
        assert len(lines) == 2
        for i, line in enumerate(lines):
            assert expected_lines[i] in line


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
