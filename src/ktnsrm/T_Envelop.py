"""
a class for envelop modulating function in time domain `g(t)`
"""


import numpy as np

class Envelop():

    def __init__(self, t):
        self.t = t # t_axis


    def get_default_envelop(self, key):
        """ a shortcut to get a modulating func by key
         
        Parameters
        ----------
        key : str,
            the name of the associated modulating function
        """
        if key == 'liam':
            return self.liam15()


    def liam15(self, b=4, c=0.8):
        """ an example modulating func cited from Liam15 """

        return b * (np.exp(-c * self.t) - np.exp(-2 * c * self.t))