"""
Inversion counting for Programming Assignment #2
"""
import logging

logger = logging.getLogger()

def from_file(f):
    """
    Return an array of integers read from a file
    
    Parameters
    ----------
    f : str
        Name of file to load integer array from

    Returns
    -------
    arr : list
        Array of integer values
    """
    with open(f, 'r') as handle:
        raw = handle.read()

    arr =  [int(i) for i in raw.splitlines()]
    logger.info("Loaded array from file %s of size %s",
                f, len(arr))
    return arr


def find_inversions(array):
    """
    Find the number of inversions in a given array

    Parameters
    ----------
    array : list
        An array of non-repeating integer values

    Returns
    -------
    inversions : int
        Number of inversions found in the array
    """
    #Counter for inversion tally
    global inversions
    inversions = 0

    #Define recursive logic
    def invert_count(array):
        #Use global inversions count
        global inversions

        #Base case of length=1 array
        if len(array) == 1 :
            logger.debug("Found instance of base case, no inversions")
            return array

        #Divide the array in half and count inversions
        half = len(array)//2
        left  = invert_count(array[:half])
        right = invert_count(array[half:])

        #Merge our sorted sub-array, counting split inversions
        merged = list()

        for k in array:
            #If either list is empty, finish
            if not left or not right:
                logger.debug("Exhausted one array, merge complete ...")
                merged.extend(left)
                merged.extend(right)
                break
            #If smallest element in left
            if left[0] < right[0]:
                merged.append(left.pop(0))

            #Smaller element in right, we have an inversion
            elif left[0] > right[0]:
                merged.append(right.pop(0))
                logger.info("Found %s inversions!", len(left))
                inversions += len(left)
        #Return our sorted array
        return merged

    #Execute recursive algorithm
    invert_count(array)
    return inversions
