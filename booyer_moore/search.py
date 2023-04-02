#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import time
import sys
from utils import get_arg


@dataclass
class Match:
    start: int
    end: int
    text: str


@dataclass
class Segment:
    start: int
    text: str


def get_text():
    if not sys.stdin.isatty():  # executed with stdin given with "|"
        return sys.stdin.read()
    else:
        with open(get_arg("--text-file"), 'r') as stream:
            return stream.read()


def split_to_segments(text: str, pattern: str, length: int = 100):

    offset = 0
    for i in range(0, len(text), length):
        seg = Segment(i, text[i+offset: length + i+offset])

        while seg.text and seg.text[-1] in pattern:
            offset += 1
            print('correct')
            seg = Segment(i, text[i: length + i + offset])

        yield seg


NO_OF_CHARS = 256000


def badCharHeuristic(string, size):
    '''
    The preprocessing function for
    Boyer Moore's bad character heuristic
    '''

    # Initialize all occurrence as -1
    badChar = [-1]*NO_OF_CHARS

    # Fill the actual value of last occurrence
    for i in range(size):
        badChar[ord(string[i])] = i

    # return initialized list
    return badChar


def search(txt, pat):
    results = []
    pattern_length = len(pat)
    text_length = len(txt)

    badChar = badCharHeuristic(pat, pattern_length)

    # s is shift of the pattern with respect to text
    pattern_shift = 0
    while (pattern_shift <= text_length-pattern_length):
        j = pattern_length-1

        # Keep reducing index j of pattern while
        # characters of pattern and text are matching
        # at this shift s
        while j >= 0 and pat[j] == txt[pattern_shift+j]:
            j -= 1

        # If the pattern is present at current shift,
        # then index j will become -1 after the above loop
        if j < 0:
            start = pattern_shift
            end = start + len(pat)
            results.append(Match(start, end, txt[start:end]))

            pattern_shift += (pattern_length - badChar[ ord( txt[pattern_shift + pattern_length] ) ]
                              if pattern_shift + pattern_length < text_length else 1)
            # print(f"pattern_shift={pattern_shift}")
        else:
            pattern_shift += max(1, j-badChar[ord(txt[pattern_shift+j])])
    return results


def align_pattern(pattern: str, text: str, i: int):
    text[i] == pattern
    start = i
    end = i + len(pattern)
    print(i)
    for occ in range(1, round((pattern.count(text[i])-1)/2)):
        print(f"occ={occ}")
        print(f"i-occ = {text[i-occ]}")

        # if text[i-occ]:

        if i+occ <= len(text)-1:
            print(f"i+occ = {text[i+occ]}")

        # for j in range(i-len(pattern), i+len(pattern)):
        #     print(text[j])
        # if text[i+1] in pattern:

    print("", end="\n")

    # for j in range(1, round(len(pattern)/2)):
    #     inj = patterntext[i+j]


def BMsearch(seg: Segment, pattern: str):
    results = []
    for i in range(len(pattern)-1, len(seg.text), len(pattern)):
        # print(f"skok-index i: {i}")
        # print(f"text[i]: {seg.text[i]}")

        if seg.text[i] in pattern:

            ind = pattern.index(seg.text[i])

            if seg.text[i] == pattern[ind]:
                start = i - ind
            # start = i-pattern.index(seg.text[i])

            # align_pattern(pattern, seg.text, i)
            # jakoś inaczej wyrównywać słowa

            end = start + len(pattern) - 1

            match = seg.text[start: end]

            if (match == pattern):
                # print("match !",end="\n\n")
                results.append(
                    Match(seg.start + start, seg.start + end, match))

    return results


if __name__ == "__main__":
    TEXT = get_text()
    PATTERN = get_arg("--pattern")

    SEGMENT_LENGTH = int(get_arg("--segment-length", 0))
    WORKERS = int(get_arg("--workers", 1)) or 1

    print(f"pattern: {PATTERN}")
    print(f"segment-length: {SEGMENT_LENGTH}")
    print(f"workers: {WORKERS}", end="\n\n")
    print("------")
    print(f"text lenght: {len(TEXT)}")

    start_time = time()

    segments = split_to_segments(TEXT, PATTERN, SEGMENT_LENGTH) if \
        SEGMENT_LENGTH > 0 else [Segment(0, TEXT)]

    with ThreadPoolExecutor(WORKERS) as exc:
        results = []
        search_jobs = [
            exc.submit(search, txt=seg.text, pat=PATTERN)
            for seg in segments
        ]

        for job in search_jobs:
            results.extend(job.result())

    print(f"work time: {(time()-start_time)*1_000} ms", end="\n\n")

    print("Results:")
    for r in results:
        print(r)

    print(f"Total count: {len(results)}")
