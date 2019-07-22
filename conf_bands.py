# by Remington Oliver Sexton 

# % matplotlib notebook
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import emcee
import corner
from scipy import optimize
from scipy import stats

def conf_bands(x,f,samples,conf=0.68):
    """ Generates confidence bands of a given fit.
    
    Computes the confidence band along a best fit function
    by computing the standard deviation of samples along the
    x-axis of a fit.
    
    Args:
        x: the x-axis of the data or the best fit function
        f: the function f(x) pertaining the best fit.  This 
            is the best fit function whose parameters are fit
            using emcee (must be same size as x).
        samples: monte-carlo fits to the data
            generated from emcee samples (see example for usage).
        conf: percentage of confidence (0,1] one wants to compute; if the number
            of samples in the flat_chain N<=30, a Student-t distribution is used, 
            and if N>30, a Normal (Gaussian) distribution is used.
    Returns:
        uci, lci: upper confidence interval, and lower confidence interval,
            centered on the best fit function provided by f.
    """
    # Check input
    if (f.size != x.size):
        raise ValueError(' x should be the same size as the best fit function f(x)!')
    if (samples[0].size != x.size):
        raise ValueError(' samples must be the same size as the array on which they are defined!')
    if  (conf >= 1) or (conf <= 0):
        raise ValueError(' chosen confidence interval must be in interval (0,99.9)!')
    print(" Computing confidence interval at %0.1f%%..." % (conf*100.0))
        
    # Compute the standard deviation along the stacked samples
    N = np.shape(samples)[0]
    print N
    # if N<=30, use a Student-t distribution to compute confidence intervals:
    if (N<=30):
        print(" Using a Student-t distribution to compute confidence intervals.")
        # Calculate standard error of the mean for all samples (along axis 0)
        sem = np.std(samples,ddof=1,axis=0)
        # iterate through best fit mean
        ucb = []
        lcb = []
        for i in range(0,len(f),1):
#             h = sem[i] * stats.t.ppf((1 + conf) / 2, N - 1)
            df = N - 1
            l,u = stats.t.interval(conf,df,loc=f[i],scale=sem[i])
#             print f[i],h
            lcb.append(l)
            ucb.append(u)
    # if N>30, use a normal (Gaussian) distribution to compute confidence intervals
    elif (N>30):
        print(" Using a normal (Gaussian) distribution to compute confidence intervals.")
        # Calculate standard error of the mean for all samples (along axis 0)
        sem = np.std(samples,axis=0)
        # iterate through best fit mean
        ucb = []
        lcb = []
        for i in range(0,len(f),1):
#             h = sem[i] * stats.t.ppf((1 + conf) / 2, N - 1)
            l,u = stats.norm.interval(conf,loc=f[i],scale=sem[i])
#             print f[i],h
            lcb.append(l)
            ucb.append(u)
        
    if 0: 
        fig = plt.figure(figsize=(5,5))
        ax1 = fig.add_subplot(1,1,1)
        ax1.plot(x,f,color='black')
        ax1.fill_between(x,ucb,lcb,color='blue',alpha=0.5)
    
    return ucb,lcb

