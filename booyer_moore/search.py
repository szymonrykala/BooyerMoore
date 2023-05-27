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
        # read the file given on '--text-file' parameter
        with open(get_arg("--text-file"), "r") as stream:
            return stream.read()


NUMBER_OF_CHARS = 256 # set of unicode code points


def __pattern_matching_chars_map(pattern: str):
    '''
        builds chars map used to match pattern in the text
    '''
    pattern_chars_map = [-1] * NUMBER_OF_CHARS

    for position, char in enumerate(pattern):
        # assign last char position in the pattern to its unicode point
        pattern_chars_map[ord(char)] = position

    return pattern_chars_map


def bm_search(txt:str, pattern: str, text_start_index: int = 0) -> Generator[tuple[int, int],None,None]:
    pattern_length = len(pattern)
    text_length = len(txt)

    pattern_chars = __pattern_matching_chars_map(pattern)

    cursor_position = 0

    # go with the cursor through the text
    while cursor_position <= text_length - pattern_length:
        char_number = pattern_length - 1

        # compare each char of the pattern starting from back
        while char_number >= 0 and pattern[char_number] == txt[cursor_position + char_number]:
            # move index to the next letter ( if pattern="lorem" -> from "m" to "e" )
            char_number -= 1 

        # if the whole pattern is a match, 'char_number' should be less than 0.
        # It means that we looped though each char of the pattern
        if char_number < 0:
            cursor_end_scope = cursor_position + pattern_length
            
            # yield a match indexes in global text context
            yield (text_start_index + cursor_position, cursor_end_scope + text_start_index)
            cursor_position += 1 

        else:
            try:
                # move cursor by the maximum from 1 and last matching 'char_number' - position of that char in the text
                cursor_position += max(1, char_number - pattern_chars[ord(txt[cursor_position + char_number])])
            except IndexError:
                # Unsupported char
                cursor_position += 1


if __name__ == "__main__":
    # reading script parameters
    TEXT = get_text()
    PATTERN = get_arg("--pattern")
    workers_count = int(get_arg("--workers", 3))

    text_length = len(TEXT)
    max_text_size = round(text_length / workers_count)

    print("-" * 20)
    print(f"pattern: {PATTERN}")
    print(f"text lenght: {len(TEXT)}")
    print(f"workers count: {workers_count}")
    print("-" * 20)

    def get_chunked_text(text: str) -> Generator[str, None, None]:        
        # list of indexes used to split the text  
        chunk_indexes = list(range( # range
            0, # from
            text_length + max_text_size, # to
            max_text_size # step
        )) # sample output = [0, 5, 10, 15]

        # enumerate through list of indexes starting from second element
        for i, text_index in enumerate(chunk_indexes[1:], 1):
            
            # until the end letter of the text chunk is present in search pattern
            while len(text) > text_index and text[text_index] in PATTERN:
                
                # expand the chunk
                text_index = chunk_indexes[i] = text_index + len(PATTERN) # update index in indexes list
            else:

                # in other case return the text chunk
                yield text[chunk_indexes[i - 1] : text_index], chunk_indexes[i - 1]


    results = []
    with ThreadPoolExecutor(workers_count) as exec:
        start_time = time()
        
        # for each text chunk, call 'bm_search' function to create async jobs
        jobs = tuple(
            exec.submit(bm_search, text_chunk, PATTERN, text_start_index) 
            for text_chunk, text_start_index in get_chunked_text(TEXT)
        )

        for job in jobs:
            # extend 'results' array with job result
            results.extend(job.result())

    end_time = time() - start_time

    # printing the results
    print("Results:")
    for start, end in sorted(results):
        print(f"index: {start}:{end}")

    print("-" * 20)
    print(f"work time: {end_time*1_000} ms", end="\n\n")
    print(f"Pattern: {PATTERN}")
    print(f"Total count: {len(results)}")
