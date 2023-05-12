#!/usr/bin/python3

import random
import string
import sys
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

import numpy as np
from booyer_moore.utils import get_arg

class Distribution(ABC):
    def __init__(self, mean: float, std_dev: float) -> None:
        super().__init__()

        self.mean = mean
        self.std_dev = std_dev

    def random(self, size):
        raise Exception('Not implemented')

class NormalDistribution(Distribution):
    def random(self, size):
        return np.random.normal(self.mean, self.std_dev, size)

class UniformDistribution(Distribution):
    def random(self, size):
        return np.random.uniform(self.mean, self.mean + self.std_dev, size)

DISTRIBUTIONS = {
    'normal': NormalDistribution,
    'uniform': UniformDistribution,
}

# Fn to make sure we output the amount of characters we need
def offset_and_scale(arr, target_sum):
    # offset to make all numbers positive
    arr = arr - np.min(arr) + 1

    # scale the array to the target sum
    arr = arr / np.sum(arr) * target_sum

    # round to integers
    arr = np.round(arr).astype(int)

    # adjust the sum if necessary
    diff = np.sum(arr) - target_sum
    if diff > 0:
        arr[np.argsort(arr)[-diff:]] -= 1
    elif diff < 0:
        arr[np.argsort(arr)[:abs(diff)]] += 1

    return arr

def generate_text(distribution: Distribution, length: int, character_set: str = string.ascii_lowercase + ' ', seed: int = None):
    if seed:
        np.random.seed(seed)

    sample = []
    character_count = offset_and_scale(distribution.random(len(character_set)), length)

    for idx, cnt in enumerate(character_count):
        sample.extend(character_set[idx] * int(cnt))

    np.random.shuffle(sample)

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

# Worth noting that it has problems with length/workers close to and lower than 1
# But it doesnt matter for our use case as we need to generate huge amount of text
# It doesnt really need to be fast so we can always lower amount of workers
if __name__ == "__main__":
    LENGTH = int(get_arg("--length"))

    MEAN = float(get_arg("--mean", 1))
    STD_DEV = float(get_arg("--std-dev", 0))
    CHARACTER_SET = get_arg("--character-set", string.ascii_lowercase + ' ')
    WORKERS = int(get_arg("--workers", 1)) or 1
    DISTRIBUTION = DISTRIBUTIONS[get_arg("--distribution", 'normal')](MEAN, STD_DEV)

    SEED = int(get_arg("--seed", 0))

    length_per_worker = round(LENGTH/WORKERS)

    with ThreadPoolExecutor(WORKERS) as exc:
        results = []
        text_generation_jobs = [
            exc.submit(generate_text, DISTRIBUTION, length, CHARACTER_SET, (SEED+i) if SEED else None)
            for i,length in enumerate(calculate_amount_of_characters_per_worker(WORKERS, LENGTH))
        ]

        for job in text_generation_jobs:
            results.append(job.result())

    results = ''.join(results)

    sys.stdout.write(results)