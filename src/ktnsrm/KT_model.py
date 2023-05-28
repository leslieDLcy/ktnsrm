""" a functional style of KT model """

import numpy as np

def parameterize_KT_model(w, wg=5 * np.pi, zzeta = 0.63, S0= 0.011):
    return S0 * (wg**4 + 4*(zzeta**2)*(wg**2)*(w**2)) / (((wg**2-w**2)**2) + 4*(zzeta**2)*(wg**2)*(w**2))


def Envelop_tfunc1(t, b=4, c=0.8):
    return b * (np.exp(-c*t) - np.exp(-2*c*t))


def get_nonsta_spectra(sta_spectra, envelop_func, t_axis):
    # sta_spectra = parameterize_KT_model(w_axis)

    gt = envelop_func(t_axis)  # envelop function in time 
    gt2 = gt**2

    # hint: S_matrix = np.outer(a_KT_spectrum, gt2)
    non_stationary_spectra = np.outer(sta_spectra, gt2)
    print(r"the shape of the nonstationary spectra $S_{wt}$:", non_stationary_spectra.shape)
    return non_stationary_spectra

