"""Utility functions for ranking posts
- HOT algorithms
- Wilson Lower-Bound approximation to Beta-Binomial
"""
import numpy as np

def intervals(upvotes, downvotes):
    a = 1. + upvotes
    b = 1. + downvotes
    mu = a / (a+b)
    std_err = 1.65 * np.sqrt( (a*b)/( (a+b)**2*(a+b+1.) ) )
    return ( mu, std_err )


