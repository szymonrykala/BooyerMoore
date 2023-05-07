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
    GROUP_SIZE = int(get_arg("--group-size", 0))
    GROUP_OVERLAPPING = get_arg("--group-overlapping", False)
    OUTPUT = get_arg("--output", "groups.png")
    SHOW = get_arg("--show", False)

    if not GROUP_SIZE > 0:
        print("Group size should be greater than 0")

    print(f"Input text: {INPUT}")

    groups = Counter(group(INPUT, GROUP_SIZE, GROUP_OVERLAPPING))
    print(f"Grouped by {GROUP_SIZE} {'' if GROUP_OVERLAPPING else 'non '}overlapping groups: {groups}")

    group_labels, group_values = zip(*sorted(groups.items(), key=lambda d: d[1]))

    plt.figure(figsize=(12,6))
    plt.bar(group_labels, group_values, width=.5, color='g') # Sorted

    plt.xticks(group_labels, group_labels, rotation='vertical')

    if SHOW:
        plt.show()
    else:
        plt.savefig(OUTPUT)