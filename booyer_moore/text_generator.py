#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import sys
import string
from typing import Iterator
import numpy as np

from utils import get_arg

def generate_text(length: int, mean: float, std_dev: float, character_set: str):
    mean = (len(character_set) - 1) / 2 if not mean else mean
    std_dev = mean / 2 if not std_dev else std_dev

    sample = ""

    for _ in range(length):
        character_weights = np.random.normal(mean, std_dev, len(character_set))
        sample += character_set[character_weights.argmax()]

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
    CHARACTER_SET = get_arg("--character-set", string.ascii_lowercase + ' ')
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