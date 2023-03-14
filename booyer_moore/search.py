#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import time
from typing import Union
import sys
import fileinput
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

    for i in range(0, len(text), length):
        offset = 0
        seg = Segment(i, text[i: length + i])
        
        while seg.text and seg.text[-1] in pattern:
            offset += 1
            seg = Segment(i, text[i: length + i + offset])

        yield seg


def search(seg: Segment, pattern: str):
    results = []
    for i in range(0, len(seg.text), len(pattern)):
        if seg.text[i] in pattern:
            start = i-pattern.index(seg.text[i])
            end = start + len(pattern)
            match = seg.text[start: end]

            if (match == pattern):
                results.append(Match(seg.start + start, seg.start + end, match))
    return results


if __name__ == "__main__":
    TEXT = get_text()
    PATTERN = get_arg("--pattern")

    SEGMENT_LENGTH = int(get_arg("--segment-length", 2_000))
    WORKERS = int(get_arg("--workers", 1)) or 1

    print(f"pattern: {PATTERN}")
    print(f"segment-length: {SEGMENT_LENGTH}")
    print(f"workers: {WORKERS}", end="\n\n")
    print("------")
    print(f"text lenght: {len(TEXT)}")

    start_time = time()

    segments = split_to_segments(TEXT, PATTERN, SEGMENT_LENGTH)

    with ThreadPoolExecutor(WORKERS) as exc:
        results = []
        search_jobs = [
            exc.submit(search, seg=seg, pattern=PATTERN)
            for seg in segments
        ]

        for job in search_jobs:
            results.extend(job.result())

    print(f"work time: {(time()-start_time)*1_000} ms", end="\n\n")

    print("Results:")
    for r in results:
        print(r)

    print(f"Total count: {len(results)}")
