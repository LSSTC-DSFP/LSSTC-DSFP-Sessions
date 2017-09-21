import numpy
import matplotlib.pyplot as plt


# ########################################
# Function
# ########################################
def from_histogram(histogram=None, bin_edges=None, ci_vals=None):
    """
    histogram:
       Should be a histogram of a PDF or whatever

    bin_edges:
       The bin edges array given back by numpy's histogram() function
       The important part is that this array has an element on the end which
          corresponds to the EDGE OF THE LAST BIN.
       Thus, len(histogram) == len(bin_edges)+1

    ci_vals:
       Credible interval values to calculate. Can be either a single number
          or a list of numbers.
    """

    # -----------------
    # Setup
    # -----------------
    assert histogram is not None
    assert bin_edges is not None
    assert ci_vals is not None

    # Make CI into list for iteration (simpler algorithm)
    try:
        num_ci_vals = len(ci_vals)
    except:
        ci_vals = [ci_vals]
        num_ci_vals = 1

    # -----------------
    # Prep Histogram
    # -----------------
    # Scalar Sum
    hist_sum = numpy.sum(histogram)
    # Cumulative Sums (backwards and forwards)
    hist_cumsum_left = numpy.cumsum(histogram)
    bin_edges_left = bin_edges
    hist_cumsum_right = numpy.cumsum(histogram[::-1])
    bin_edges_right = bin_edges[::-1]


    # ---------------------------
    # Loop Through Interval Level
    # ---------------------------
    results = ()
    for ci in ci_vals:

        # Calculate Fraction of 
        # ---------------------
        # Fraction to move in from the end
        ci_half_fraction = (1.0-ci)/2.0
        ci_half_hist_sum = ci_half_fraction * hist_sum

        # From Left
        # ----------------
        # Subscript of correct bin
        left_bin_sub = numpy.searchsorted(hist_cumsum_left, ci_half_hist_sum, side='left')
        # Linear interpolation
        dx_left =  bin_edges_left[left_bin_sub + 1] - bin_edges_left[left_bin_sub]
        dy_left = hist_cumsum_left[left_bin_sub] - hist_cumsum_left[left_bin_sub - 1] 
        # Line in Point-Slope Form
        from_left = (dx_left/float(dy_left))*(ci_half_hist_sum - hist_cumsum_left[left_bin_sub-1]) + bin_edges_left[left_bin_sub]

        # From Right
        # ----------------
        # Subscript of correct bin
        right_bin_sub = numpy.searchsorted(hist_cumsum_right, ci_half_hist_sum, side='left')
        # Linear interpolation (searchsorted finds index of bin that is one too high)
        dx_right =  bin_edges_right[right_bin_sub + 1] - bin_edges_right[right_bin_sub]
        dy_right = hist_cumsum_right[right_bin_sub] - hist_cumsum_right[right_bin_sub - 1] 
        # Line in Point-Slope Form
        from_right = (dx_right/float(dy_right))*(ci_half_hist_sum - hist_cumsum_right[right_bin_sub-1]) + bin_edges_right[right_bin_sub]

        # Put into Results Tuple
        # -----------------------
        results += (from_left, from_right),

    return results


# ########################################
# Command-Line Test Code
# ########################################
if __name__ == '__main__':    

    # ===================================
    # Make Fake Data
    # ===================================

    # Parameter Values
    # -----------------
    # Number of Randoms
    N = 2190
    # Normal Dist Parameters
    mu = 2.54
    sigma = 0.57
    # Binning
    bin_size = 0.217
    bin_min = mu - 5*sigma 
    bin_max = mu + 5*sigma 
    # 
    num_bins = int((bin_max-bin_min)/bin_size)

    # Generate Histogram
    # --------------------
    # Generate Randoms
    rand_array = numpy.random.normal(size=N, loc=mu, scale=sigma)
    # Bin Into Histogram
    #hist, edges = numpy.histogram(rand_array, bins=num_bins, range=[bin_min,bin_max])
    hist, edges = numpy.histogram(f_hiy_full2)


    # ====================================
    # Credible Interval Results
    # ====================================

    # Calculate Results
    # ----------------------
    # Credible Interval Vals
    ci = [0.6827, 0.9545]    
    # Call CI-Calculating Function
    results = from_histogram(histogram=hist, bin_edges=edges, ci_vals=ci)

    # ------------------
    # Print Results
    # ------------------
    for i,c in enumerate([1,2]):
        print
        print 'Interval Val: ',ci[i]
        print '   Expected Low:', mu - c*sigma
        print '      Calculated Low:', results[i][0]
        print '   Expected High:', mu + c*sigma
        print '      Calculated Hight:', results[i][1]

    print

