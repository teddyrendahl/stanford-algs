############
# Standard #
############
import logging

############
# External #
############
import numpy as np

###########
# Package #
###########

logger = logging.getLogger(__name__)

def from_file(f):
    """
    Load an array from a given file
    """
    with open(f, 'r') as handle:
        #Read array
        arr = handle.read().split('\n')
        #Clean array
        arr = [int(i) for i in arr if i!='']
    return arr

def select_first(arr, l, r):
    """
    Select the first element of a subarray to use as a pivot
    """
    return l

def select_last(arr, l, r):
    """
    Select the last element of a subarry to use as a pivot
    """
    return r

def select_threepoint_median(arr, l, r):
    """
    Select the median value from a three sample subarray to use as a pivot
    """
    #Available indexes
    idxs = [l, r, l+(r-l)//2]
    vals = [arr[idx] for idx in idxs]
    return idxs[vals.index(np.median(vals))]

def quicksort(arr, choose_pivot):
    """
    Sort an array using the QuickSort Algorithm

    This instantiatiation also counts the total number of comparisons necessary
    for the algorithm to complete

    Parameters
    ----------
    arr : list
        Array to sort

    choose_pivot : func
        Function used to choose the pivot point of QuickSort. Expected
        signature receive an input an array and return the index of the chosen
        pivot

        .. code::

            f(arr, l, r) -> int

    Returns
    -------
    comparisons : int
        Number of comparisons necessary for quicksort completion
    """
    #Instantiate comparison tracker
    global comparisons
    comparisons = 0

    def partition(arr, l, r):
        #Add to our total number of comparisons (len(sub_arr) -1)
        global comparisons
        comparisons += max(r-l, 0)
        logger.info("Sorting elements %s to %s", l, r)
        logger.info("Total number of comparisons %s", comparisons)

        #Base Case
        if r - l < 1:
            logger.info("Reached base case!")
            return

        #Select pivot and swap to front
        i_p = choose_pivot(arr, l, r)
        logger.info("Chose %s as our pivot point ...", arr[i_p])
        arr[l], arr[i_p] = arr[i_p], arr[l]

        #Partition the array around the pivot
        i = l+1
        for j in range(l+1, r+1):
            #If our newly seen value is less than the pivot
            if arr[j] < arr[l]:
                #Swap
                logger.debug("Swapping elements at indexes %s and %s", i, j)
                arr[i], arr[j] = arr[j], arr[i]
                #Increment our partition on seen array elements
                i += 1
        #Place our pivot in the partition
        logger.info("Array element %s belongs at index %s", arr[l], i-1)
        arr[l], arr[i-1] = arr[i-1], arr[l]

        #Recursively call partition on sub-array
        if i!=l+1:
            partition(arr, l, i-2)
        partition(arr, i, r)

    #Call partition on full array
    partition(arr, 0, len(arr)-1)
    #Return total number of comparisons needed
    return comparisons
