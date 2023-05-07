#!/usr/bin/python3

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import sys
import string
from typing import Iterator
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

from utils import get_arg

from itertools import groupby

def group(text: str, group_size: int, overlapping: bool = False):
    assert group_size > 0

    result = []

    for i in range(0, len(text), 1 if overlapping else group_size):
        result.append(text[i:i+group_size])

    return result

if __name__ == "__main__":
    INPUT = get_arg("--input", "") or sys.stdin.read()

    print(f"Generated text: {INPUT}")

    for i in range(1, 6):
        for overlapping in [False, True]:
            groups = group(INPUT, i, overlapping)
            print(f"Grouped by {i} {'' if overlapping else 'non '}overlapping groups: {groups}")