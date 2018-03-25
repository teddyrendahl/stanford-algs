import copy
import heapq

from collections import namedtuple


Symbol = namedtuple('Symbol', ('weight', 'index'))


def from_file(path):
    with open(path, 'r') as handle:
        nodes = [int(line) for line in handle.readlines()[1:]]
    return nodes


def metasymbol(a, b):
    """Create the name of a new metasymbol"""
    return '+'.join([str(a), str(b)])


def component_symbols(symbol):
    """Find all component symbols of a metasymbol"""
    return [int(i) for i in str(symbol).split('+')]


def huffman(weights):
    """
    Return the number of bits needed to encode all of an alphabet
    """
    # Create our data structures
    symbols = [1] * len(weights)
    tree = [Symbol(weight, str(i)) for i, weight in enumerate(weights)]
    heapq.heapify(tree)
    while len(tree) > 2:
        # Find the two lowest items
        a = heapq.heappop(tree)
        b = heapq.heappop(tree)
        # Add our new metanode
        heapq.heappush(tree, Symbol(a.weight + b.weight,
                                    metasymbol(a.index, b.index)))
        # Note that we have one more level of depth for all component nodes
        components = [node for metanode in (a, b)
                           for node in component_symbols(metanode.index)]
        for component in components:
            symbols[component] += 1

    return symbols


