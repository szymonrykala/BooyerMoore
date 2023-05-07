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

if __name__ == "__main__":
    INPUT = get_arg("--input", "") or sys.stdin.read()
    OUTPUT = get_arg("--output", "foo.png")

    h: np.ndarray = np.fromiter(bytes(INPUT, 'ascii'), dtype=int)
    # h: np.ndarray = np.sort(np.fromiter(bytes(INPUT, 'ascii'), dtype=int))
    # h: np.chararray = np.char.array(np.fromiter(INPUT, (np.unicode_,1)))
    # print(h.mean())
    # hstd = np.std(h)
    # pdf = stats.norm.pdf(h, h.mean(), h.std())
    # counts, bins = np.histogram(h)
    # plt.stairs(counts, bins)
    # pdf = plt.hist(h)
    # plt.plot(h, pdf) # including h here is crucial

    c = Counter(INPUT)
    plt.bar(*zip(*sorted(c.items(), key=lambda d: d[1])), width=.5, color='g') # Sorted
    # plt.bar(*zip(*c.items()), width=.5, color='g') # Non Sorted
    # plt.show()
    plt.savefig(OUTPUT)