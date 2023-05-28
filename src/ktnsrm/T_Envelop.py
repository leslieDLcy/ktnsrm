"""
a class for envelop modulating function in time domain `g(t)`
"""
import numpy as np
from functools import partial

class Envelop():

    def __init__(self, t):
        self.t = t # t_axis


    def get_envelop(self, key, **kwargs):
        """ a shortcut to get a modulating func by key
         
        Parameters
        ----------
        key : str,
            the name of the associated modulating function
        """
        if key == 'liam15':
            return partial(self.liam15, **kwargs)


    def liam15(self, b=4, c=0.8):
        """ an example modulating func cited from Liam15 """

        return b * (np.exp(-c * self.t) - np.exp(-2 * c * self.t))