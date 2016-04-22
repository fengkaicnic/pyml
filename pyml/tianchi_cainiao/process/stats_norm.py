from scipy import stats
from scipy.stats import kstest

import numpy as np

nr = stats.norm(0, 1)

data = np.random.normal(0, 1, 25)

statics , p_value = kstest(data, 'norm')

print nr.cdf(0.75)

print p_value
