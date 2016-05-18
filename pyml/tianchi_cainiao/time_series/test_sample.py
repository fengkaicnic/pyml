import numpy as np
import statsmodels.api as sm
import pandas as pd
import pdb
from statsmodels.tsa.arima_process import arma_generate_sample
import traceback

np.random.seed(12345)

pdb.set_trace()
arparams = np.array([.75, -.25])
maparams = np.array([.65, .35])

arparams = np.r_[1, -arparams]
maparam = np.r_[1, maparams]
nobs = 25

try:
    y = arma_generate_sample(arparams, maparams, nobs)
except:
    traceback.print_exc()


dates = sm.tsa.datetools.dates_from_range('1980m1', length=nobs)
y = pd.TimeSeries(y, index=dates)
arma_mod = sm.tsa.ARMA(y, order=(2,2))
arma_res = arma_mod.fit(trend='nc', disp=-1)

print(arma_res.summary())


