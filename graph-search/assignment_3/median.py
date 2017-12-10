############
# Standard #
############
import math
import heapq
import logging

logger = logging.getLogger(__name__)


def number_stream(path):
    """
    Generator that yields a number at a time from an input file

    Parameters
    ----------
    path : str
        Filename
    """
    with open(path, 'r') as f:
        for line in f.readlines():
            yield int(line)


def median_maintenance(number_stream):
    """
    Calculate the sum of all m_k mod 10000

    Using heaps, request a new entry from our number stream, calculate the
    median of all points we have collected so far, and add it to our tally.
    Keep track of this until we have exhausted our stream and return the sum
    of all medians mod 10000

    Parameters
    ----------
    number_stream : iterator
        Stream of numbers

    Returns
    -------
    sum : int
        Sum off all median values calculated mod 10000
    """
    # Create our data structures
    start = (next(number_stream), next(number_stream))
    logger.info("Starting with %s", start)
    small = [-min(start)]
    large = [max(start)]
    median_sum = start[0] + min(start)
    while True:
        # Grab the next number of our stack
        try:
            _next = next(number_stream)
        # If we have exhausted our stream, exit loop
        except StopIteration:
            break
        # Add our new value to the appropriate heap
        logger.info("Adding new value %s ...", _next)
        if _next > -min(small):
            heapq.heappush(large, _next)
        else:
            heapq.heappush(small, -_next)
        logger.debug("Heaps look like ... ")
        logger.debug(small)
        logger.debug(large)
        # Rebalance our heaps
        size_diff = len(large) - len(small)
        if size_diff > 1:
            heapq.heappush(small, -heapq.heappop(large))
        # Rebalance our heaps if necessary
        elif size_diff < -1:
                heapq.heappush(large, -heapq.heappop(small))
        logger.debug("After rearrangment heaps look like ...")
        logger.debug(small)
        logger.debug(large)
        # Take median from the larger array, if they are the same take from
        # small
        heaps = sorted([large, small], key=lambda x: len(x))
        median = int(math.fabs(min(heaps[1])))
        # Add to our tally
        logger.info("Found median %s!", median)
        median_sum += median
    # Return final calculation mod 10000
    return median_sum % 10000
