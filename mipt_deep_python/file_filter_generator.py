from typing import IO, Generator, List, TextIO, Union


def filter_lines(
    file: Union[str, TextIO],
    search_words: List[str],
    stop_words: List[str],
) -> Generator[str, None, None]:
    search_set = {word.lower() for word in search_words}
    stop_set = {word.lower() for word in stop_words}

    if isinstance(file, str):
        with open(file, "r", encoding="utf-8") as file_obj:
            yield from _process_lines(file_obj, search_set, stop_set)
    else:
        file.seek(0)
        yield from _process_lines(file, search_set, stop_set)


def _process_lines(
    file_obj: IO,
    search_set: set,
    stop_set: set,
) -> Generator[str, None, None]:
    for line in file_obj:
        line = line.strip()
        if not line:
            continue

        words_in_line = line.lower().split()
        words_set = set(words_in_line)

        if words_set & stop_set:
            continue

        if words_set & search_set:
            yield line
