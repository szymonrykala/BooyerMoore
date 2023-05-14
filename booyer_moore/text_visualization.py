#!/usr/bin/python3

from collections import Counter
import sys
import matplotlib.pyplot as plt

from utils import get_arg

if __name__ == "__main__":
    INPUT = get_arg("--input", "") or sys.stdin.read()
    OUTPUT = get_arg("--output", "foo.png")

    c = Counter(INPUT)
    plt.bar(*zip(*sorted(c.items(), key=lambda d: d[1])), width=.5, color='g') # Sorted
    # plt.bar(*zip(*c.items()), width=.5, color='g') # Non Sorted
    # plt.show()
    plt.savefig(OUTPUT)