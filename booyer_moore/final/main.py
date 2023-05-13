from collections import Counter
import os

from matplotlib import pyplot as plt
from booyer_moore.text_generator import generate_text, NormalDistribution
from booyer_moore.text_grouping import group
import numpy as np

LENGTH = 10000
DISTRIBUTION = NormalDistribution(mean=0.0, std_dev=1.0)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEXT_FILE_PATH = os.path.join(CURRENT_DIR, 'text.txt')
GROUP_OVERLAPPING = False
GROUP_LIST = {2: ('dwuznakowe', 'cornflowerblue'), 3: ('trójznakowe', 'orange'), 4: ('czworoznakowe', 'green'), 5: ('pięcioznakowe', 'red')}
SINGLE_PLOT = False
IGNORE_TEXTFILE = False

if __name__ == "__main__":
    if IGNORE_TEXTFILE:
        text = generate_text(DISTRIBUTION, LENGTH)
    else:
        if not os.path.isfile(TEXT_FILE_PATH):
            text = generate_text(DISTRIBUTION, LENGTH)
            with open(TEXT_FILE_PATH, 'w') as file:
                file.write(text)
        else:
            with open(TEXT_FILE_PATH, 'r') as file:
                text = file.read()


    c = Counter(text)
    plt.bar(*zip(*sorted(c.items(), key=lambda d: d[1])), width=.5, color='g') # Sorted
    plt.savefig(os.path.join(CURRENT_DIR, 'letters.png'))
    plt.clf()

    def plot_groups(groups, fname):
        groups_data = {}
        max_count = 0
        min_count = 1000000
        for group_size in groups.keys():
            g = {}

            group_counts = Counter(group(text, group_size, overlapping=GROUP_OVERLAPPING))
            group_labels, group_values = zip(*sorted(group_counts.items(), key=lambda d: d[1]))
            groups_grouped = Counter(group_values)
            group_labels, group_values = zip(*sorted(groups_grouped.items(), key=lambda d: d[1]))
            for i in range(0, len(group_labels)):
                label = group_labels[i]
                value = group_values[i]
                g[label] = value

            curr_max_count = max(group_labels)
            curr_min_count = min(group_labels)
            if max_count < curr_max_count:
                max_count = curr_max_count

            if min_count > curr_min_count:
                min_count = curr_min_count

            groups_data[group_size] = g

        width = 0.17
        multiplier = 0
        counts = np.arange(min_count, max_count+1)

        fig, ax = plt.subplots(layout='constrained')
        fig.set_size_inches(12,6)
        ax.set_ymargin(0.1)
        ax.set_ylabel('Ilość grup')
        ax.set_xlabel('Liczba wystąpień grupy w tekście')
        ax.set_title('Liczba grup o danej ilości wystąpień w tekście')

        for group_size, group_values in groups_data.items():
            group_prefix, group_color = groups[group_size]
            group_name = f'Grupy {group_prefix}'
            offset = width * multiplier
            values = []
            for i in counts:
                values.append(group_values.get(i, np.NaN))
            rects = ax.bar(counts + offset, values, width, label=group_name, align='center', color=group_color)
            ax.bar_label(rects, padding=3)#, rotation='vertical')
            multiplier += 1
            ax.legend(loc='upper right', ncols=1)
            ax.set_xticks(counts + (width*(len(groups)/2-0.5)), counts)

            # if SINGLE_PLOT:
            #     fig.savefig(os.path.join(CURRENT_DIR, f'group_{group_size}_chart.png'))
            #     ax.clear()

        # ax.set_ylim(0, 250)
        fig.savefig(os.path.join(CURRENT_DIR, fname))

    # plot_groups(GROUP_LIST, 'group_chart.png')
    for k,v in GROUP_LIST.items():
        plot_groups({k: v}, f'group_{k}_chart.png')


    # plt.figure(figsize=(12,6))
    # offset = 0
    # for group_size, group_color, group_suffix in [(2, 'g', 'dwuznakowa'),(3, 'b', 'trójznakowa'),(4, 'orange', 'czworoznakowa'),(5, 'yellow', 'pięcioznakowa')]:
    #     offset +=0.3
    #     h: np.ndarray = np.fromiter(bytes(text, 'ascii'), dtype=int)

    #     groups = Counter(group(text, group_size, overlapping=GROUP_OVERLAPPING))
    #     group_labels, group_values = zip(*sorted(groups.items(), key=lambda d: d[1]))

    #     # plt.figure(figsize=(12,6))
    #     # plt.bar(group_labels, group_values, width=.5, color='g') # Sorted

    #     # plt.xticks(group_labels, group_labels, rotation='vertical')

    #     # plt.savefig(os.path.join(CURRENT_DIR, f'group_{group_size}.png'))

    #     groups_grouped = Counter(group_values)
    #     group_labels, group_values = zip(*sorted(groups_grouped.items(), key=lambda d: d[1]))

    #     bar = plt.bar(group_labels, group_values, width=0.5, color=group_color) # Sorted
    #     bar.set_label(f'Grupa {group_suffix}')

    # plt.ylabel('Ilość grup')
    # plt.xlabel('Liczba wystąpień grupy w tekście')
    # # plt.xticks(group_labels, group_labels)#, rotation='vertical')
    # plt.legend()

    # plt.savefig(os.path.join(CURRENT_DIR, f'group_chart.png'))