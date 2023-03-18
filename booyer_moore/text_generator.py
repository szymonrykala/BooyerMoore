#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import random
import sys
import string
from typing import Iterator

from utils import get_arg

def offset(array: list[int], offset = 1) -> list[int]:
    return [z - min(array) + offset for z in array] if min(array) < 1 else array # no need for ofset if we have positive numbers

def generate_text(length: int, mean: float, std_dev: float, character_set: str):
    mean = (len(character_set) - 1) / 2 if not mean else mean
    std_dev = mean / 2 if not std_dev else std_dev

    # random.choices weights sum needs to be greater than 0, so offset them so its always the case
    weights = offset([random.normalvariate(mean, std_dev) for _ in range(len(character_set))])

    sample = random.choices(
        character_set,
        weights=weights,
        k=length
    )

    return ''.join(sample)

def calculate_amount_of_characters_per_worker(num_workers: int, num_char: int) -> Iterator[int]:
    # calculate the number of jobs each worker should get
    jobs_per_worker = num_char // num_workers
    remainder = num_char % num_workers

    # assign the jobs to the workers
    for i in range(num_workers):
        if i < remainder:
            assignments = jobs_per_worker + 1
        else:
            assignments = jobs_per_worker

        yield assignments

if __name__ == "__main__":
    LENGTH = int(get_arg("--length"))

    MEAN = float(get_arg("--mean", 0))
    STD_DEV = float(get_arg("--std-dev", 0))
    CHARACTER_SET = get_arg("--character-set", string.ascii_letters + ' ')
    WORKERS = int(get_arg("--workers", 1)) or 1

    length_per_worker = round(LENGTH/WORKERS)

    with ThreadPoolExecutor(WORKERS) as exc:
        results = []
        text_generation_jobs = [
            exc.submit(generate_text, words_per_worker, MEAN, STD_DEV, CHARACTER_SET)
            for words_per_worker in calculate_amount_of_characters_per_worker(WORKERS, LENGTH)
        ]

        for job in text_generation_jobs:
            results.append(job.result())

    sys.stdout.write(''.join(results))
    sys.stdout.write('\n')