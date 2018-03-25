import copy
from collections import namedtuple

import numpy as np

Item = namedtuple('Item', ('weight', 'value'))


def from_file(path):
    with open(path, 'r') as handle:
        lines = handle.readlines()
        size, item_length = lines.pop(0).split()
        items = list()
        for line in lines:
            value, weight = line.split()
            items.append(Item(int(weight), int(value)))
        return int(size), items


def knapsack(size, items):
    """Find the greatest value of items you can place in the knapsack"""
    A = np.zeros((len(items)+1, size+1))
    for i, item in enumerate(items):
        for x in range(size+1):
            # Value if we do not include this item
            not_added = A[i][x]
            # Value if we do include this item
            if item.weight <= x:
                added = A[i][x-item.weight] + item.value
            else:
                added = 0
            # Remember the optimal value
            A[i+1][x] = max(not_added, added)
    return A[len(items)][size]


def fast_knapsack(size, items):
    best_weights = np.zeros(size+1)
    item_weights = np.zeros(size+1)
    for i, item in enumerate(items):
        # If we can not add the item just use the last row
        item_weights[:item.weight] = best_weights[:item.weight]
        for x in range(item.weight, size+1):
            # Value if we do not include this item
            not_added = best_weights[x]
            # Value if we do include this item
            added = best_weights[x-item.weight] + item.value
            # Remember the optimal value
            if added > not_added:
                item_weights[x] = added
        best_weights = copy.copy(item_weights)
    return best_weights[-1]
