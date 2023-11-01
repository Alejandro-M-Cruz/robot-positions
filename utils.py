import random
from typing import Iterable, Sequence

import matplotlib.pyplot as plt


def store_to_file(values: Iterable, file_path: str):
    with open(file_path, 'w') as file:
        file.write('\n'.join(map(str, values)))


def introduce_gaussian_error(values: Sequence[float]):
    mean = 0
    std = (sum(values) / len(values)) * 0.01
    return tuple(value + random.gauss(mean, std) for value in values)


def plot(x_values: Sequence[float], y_values: Sequence[float], *, title: str, x_label='x', y_label='y'):
    plt.plot(x_values, y_values)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
