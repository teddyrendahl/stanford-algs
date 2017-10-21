"""
Karatsuba Multplication Algorithm implemented in Python
"""
import logging

logger = logging.getLogger(__name__)

def karatsuba(x, y):
    """
    Return the product of two integers x and y

    Parameters
    ----------
    x : str, int

    y : str, int

    Returns
    -------
    z : int
        Product of x and y
    """
    #Clean input
    x, y = int(x), int(y)

    logger.info("Running karatsuba multiplication for %s, %s",
                 x, y)
    #Base case of single integer multiplication
    if x < 10 and y < 10:
        logger.debug("Using base case, simple multiplication")
        return x*y
    #Select our scale
    m  = max(len(str(x)), len(str(y)))//2
    b  = 10**m

    #Create two smaller integers by decomposing by the base
    def decompose(v):
        v0, v1 = v//b, v%b
        logger.debug("Decomposed %s into -> %s, %s",
                     v, v0, v1)
        return v0, v1
    x0, x1 = decompose(x)
    y0, y1 = decompose(y)

    #Perform three multiplication steps, recursively calling karatsuba
    z0 = karatsuba(x1, y1)
    z2 = karatsuba(x0, y0)
    z1 = karatsuba(x0+x1, y0+y1) - z0 - z2 #Replaces x1*y0 + x0*y1

    return z2*b**2 + z1*b + z0
