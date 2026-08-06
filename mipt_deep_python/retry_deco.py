from functools import wraps
from typing import Any, Callable, List, Optional, Type


def retry_deco(
    max_retries: int = 1,
    expected_exceptions: Optional[List[Type[Exception]]] = None,
) -> Callable:
    if expected_exceptions is None:
        expected_exceptions = []

    expected_exceptions_tuple = tuple(expected_exceptions)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            function_name = func.__name__

            args_parts = []
            if args:
                args_parts.append(f"positional args = {args}")
            if kwargs:
                args_parts.append(f"keyword kwargs = {kwargs}")

            args_info = ", ".join(args_parts)

            call_info = f'run "{function_name}" with {args_info}'

            print(call_info)

            last_exception = None

            for attempt in range(1, max_retries + 2):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f"{call_info}, attempt = {attempt}, result = {result}",
                    )
                    return result

                except expected_exceptions_tuple as e:
                    print(
                        call_info
                        + ", attempt = "
                        + str(attempt)
                        + ", exception = "
                        + type(e).__name__,
                    )
                    raise e

                except Exception as e:
                    last_exception = e
                    print(
                        call_info
                        + ", attempt = "
                        + str(attempt)
                        + ", exception = "
                        + type(e).__name__,
                    )

                    if attempt == max_retries + 1:
                        raise e

            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected error in retry decorator")

        return wrapper

    return decorator
