#!/usr/bin/python3

import sys
from concurrent.futures import ThreadPoolExecutor
from time import time
from typing import Generator

from utils import get_arg


def get_text():
    if not sys.stdin.isatty():  # executed with stdin given with "|"
        return sys.stdin.read()
    else:
        with open(get_arg("--text-file"), "r") as stream:
            return stream.read()


NO_OF_CHARS = 256


def __pattern_matching_chars_map(string, size):
    pattern_chars_map = [-1] * NO_OF_CHARS

    for i in range(size):
        pattern_chars_map[ord(string[i])] = i

    return pattern_chars_map


def search(txt, pattern) -> Generator[tuple[int, int], None, None]:
    pattern_length = len(pattern)
    text_length = len(txt)

    pattern_chars = __pattern_matching_chars_map(pattern, pattern_length)

    cursor_position = 0
    while cursor_position <= text_length - pattern_length:
        j = pattern_length - 1

        while j >= 0 and pattern[j] == txt[cursor_position + j]:
            j -= 1

        if j < 0:
            yield (cursor_position, cursor_position + pattern_length)

            if cursor_position + pattern_length < text_length:
                cursor_position += pattern_length - pattern_chars[ord(txt[cursor_position + pattern_length])]
            else:
                cursor_position += 1

        else:
            try:
                cursor_position += max(1, j - pattern_chars[ord(txt[cursor_position + j])])
            except IndexError:
                # Unsupported char
                cursor_position += 1


if __name__ == "__main__":
    TEXT = get_text()
    PATTERN = get_arg("--pattern")

    workers = int(get_arg("--workers", 2))

    text_length = len(TEXT)
    # max_text_size = 38_000_000
    max_text_size = round(text_length / workers)

    print("-" * 20)
    print(f"pattern: {PATTERN}")
    print(f"text lenght: {len(TEXT)}")
    print("-" * 20)

    def get_chunked_text(text: str) -> list[str]:
        l = list(range(1, text_length, max_text_size))
        fragments = []
        for i, num in enumerate(l[1:], 1):
            while text[num] in PATTERN:
                l[i] += len(PATTERN)
                num += len(PATTERN)
            else:
                fragments.append(text[l[i - 1] : num])

        return fragments

    if text_length > max_text_size:
        text_list = get_chunked_text(TEXT)
    else:
        text_list = (TEXT,)

    results = []

    with ThreadPoolExecutor(round(text_length / max_text_size) or 1) as exec:
        start_time = time()
        jobs = tuple(exec.submit(search, text_chunk, PATTERN) for text_chunk in text_list)

        for job in jobs:
            results.extend(job.result())

    end_time = time() - start_time

    print("Results:")
    for start, end in results:
        print(f"index: {start}:{end}")

    print("-" * 20)
    print(f"work time: {end_time*1_000} ms", end="\n\n")
    print(f"Pattern: {PATTERN}")
    print(f"Total count: {len(results)}")
