#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import time
from typing import Union
import sys
import fileinput


@dataclass
class Match:
    start: int
    end: int
    text: str


@dataclass
class Segment:
    start: int
    text: str


def get_arg(name: str, default: Union[str, int, None] = None):
    if name not in sys.argv:
        if default:
            return default
        else:
            print(f"Argument '{name}' is required to run the script")
            exit(1)

    index = sys.argv.index(name)
    return sys.argv[index+1]


def get_text():
    if not sys.stdin.isatty():  # executed with stdin given with "|"
        return sys.stdin.read()
    else:
        with open(get_arg("--text-file"), 'r') as stream:
            return stream.read()


def split_to_segments(text: str, pattern: str, length: int = 100):
    offset = 0

    for i in range(0, len(text), length):
        seg = Segment(i+offset, text[i + offset: length + i + offset])

        while seg.text and seg.text[-1] in pattern:
            offset += len(pattern)
            seg = Segment(i, text[i: length + i + offset])

        yield seg


def search(seg: Segment, pattern: str):
    # print(f"Start job: {pattern} {seg}")
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

    SEGMENT_LENGTH = int(get_arg("--segment-length", 100))
    SEGMENTS_PER_WORKER = int(get_arg("--segments-per-worker", 2))
    WORKERS = round(len(TEXT) / (SEGMENT_LENGTH*SEGMENTS_PER_WORKER))
    WORKERS = 1 if WORKERS == 0 else WORKERS

    print(f"pattern: {PATTERN}")
    print(f"segment-length: {SEGMENT_LENGTH}")
    print(f"segments-per-worker: {SEGMENTS_PER_WORKER}")
    print("------")
    print(f"text lenght: {len(TEXT)}")
    print(f"workers number: {WORKERS}", end="\n\n")

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
