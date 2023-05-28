"""
Introduction
============
* implementation for the Kanai Tajimi model and also
* implementation for Spectral Representation method by Shinozuka
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import itertools
import pandas as pd
from scipy import interpolate
from scipy.interpolate import griddata
from ktnsrm.utils import EPSD_show


class SRM:
    def __init__(self, wu=100, N1=1024, fs=200, duration=16):
        self.wu = wu
        self.N1 = N1        
        self.fs = fs
        self.duration = duration
    # print('the cutoff frequency wu set as:', wu)
        self.t_axis_4simu = np.arange(0, self.duration, 1 / self.fs)  # dt = 1 / Fs
        self.w_axis_4simu = np.arange(0, self.wu, self.wu/self.N1)


    def __str__(self):
        return f'Frequency axis shape is {self.w_axis_4simu.shape} and Time axis shape is {self.t_axis_4simu.shape}'

    # @property
    # def t_axis_4simu(self):
    #     """Create the t-axis of the sample simulation"""
    #     t_axis_simu = np.arange(0, self.duration, 1 / self.fs)  # dt = 1 / Fs
    #     return t_axis_simu


    # # set up the w (rad/s) axis
    # @property
    # def w_axis_4simu(self):
    #     w_axis = np.arange(0, self.wu, self.wu/self.N1)
    #     return w_axis 

    def _SpecRepsentation0(self, Sww, plotting=True):
        ''' SRM for stationary PSD

        For now, this func received a spectra as argument,
        which may be obtained from 'getSww_from_a_model' func
        '''
    
        # create the t axis
        n = np.arange(self.N1)
        delta_w = self.wu / self.N1
        w_n = n * delta_w
        A_n = np.sqrt(2 * Sww * delta_w)
        phi_n = np.random.uniform(0, 2 * np.pi, self.N1)
    
        # Note that A0=0 or S(w0)=0
        sum = 0
        for i in range(1, self.N1):
            sum = sum + A_n[i] * np.cos(w_n[i] * self.t_axis_4simu + phi_n[i])
        simulation = sum * np.sqrt(2)
        # print('sampling frequency:', Fs)
        t_upper_limit = 2 * np.pi / (2 * self.wu)
        print("the lower limit of sampling frequency:", math.ceil(1 / t_upper_limit))
        print("the length of the simulation", simulation.shape)
        if plotting:
            fig, ax = plt.subplots()
            ax.plot(self.t_axis_4simu, simulation)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude')
        return simulation


    @staticmethod
    def getSww_from_a_model(model, w_axis):
        return model(w_axis)



    def _interpo_spectra(self, Pxx, freqs, t_bins, plotting=True, format='2d', title_name='interpolated_spectra'):
    
        """
        Given Swt estimated by STFT, 
        ie. Pxx, freqs, t_bins, im = ax2.specgram(...)
        
        Follow the example procedures;
        # Points, values, and then new coordinates
        """
        points  = list(itertools.product(t_bins, freqs))
        sample_df = pd.DataFrame()
        sample_df['X'] = [xy[0] for xy in points]
        sample_df['Y'] = [xy[1] for xy in points]
    
        up_reversed = np.flipud(Pxx)
        values = np.ravel(up_reversed, order='F')
    
        x_min, x_max = 0.0, sample_df['X'].max()
        y_min, y_max = 0.0, sample_df['Y'].max()
    
        new_x_coord = np.linspace(x_min, x_max, self.duration * self.fs)
        new_y_coord = np.linspace(y_min, y_max, self.N1)
        xx, yy = np.meshgrid(new_x_coord, new_y_coord)
    
        grid_z0 = griddata(points, values, xi=(xx, yy), method='nearest')
        grid_z1 = np.flipud(grid_z0)
        
        self._interpolated_bundle = (grid_z1, new_y_coord, new_x_coord)
        # if plotting:
        #     # plotting the Swt on new axes
        #     EPSD_show(grid_z1, new_y_coord, new_x_coord, format=format, title_name=title_name)
        return grid_z1
    


    def _get_interpolated_spectra(self, format):
        EPSD_show(*self._interpolated_bundle, format=format, title_name='interpolated spectra')
        # plt.show()       

    

    def nonsta_simulation(self, Pxx, freqs, t_bins, plotting=False):
        """
        For given estimated spectra, do interpolation first and then do simulation;
        
        Paramters:
        ---------
        Pxx, freqs, t_bins: 
        Given the estimated spectra by STFT

        **kwargs :
        Used to control if showing the estimated spectra in 2d or 3d
        """
        interpolated_Swt = self._interpo_spectra(Pxx, freqs, t_bins)
        x = self._SpecRepsentation0(interpolated_Swt, plot='y')
        return x


    def SpecRepsentation3(self, Sww, t_bins, plot='y'):
        '''
        For now, this func received a spectra as argument,
        which may be obtained from 'getSww_from_a_model' func
        '''
    
        # create the t axis
        n = np.arange(self.N1)
        delta_w = self.wu / self.N1
        w_n = n * delta_w
        A_n = np.sqrt(2 * Sww * delta_w)
        phi_n = np.random.uniform(0, 2 * np.pi, self.N1)
    
        # Note that A0=0 or S(w0)=0
        sum = 0
        for i in range(1, len(Sww)):
            f = interpolate.interp1d(t_bins, 
                 A_n[i], 
                 kind='next', 
                 bounds_error=False, 
                 fill_value='extrapolate')

            A_new = f(self.t_axis_4simu)
            sum = sum + A_new * np.cos(w_n[i] * self.t_axis_4simu + phi_n[i])

        simulation = sum * np.sqrt(2)
        # print('sampling frequency:', Fs)
        t_upper_limit = 2 * np.pi / (2 * self.wu)
        print("the lower limit of sampling frequency:", math.ceil(1 / t_upper_limit))
        print("the length of the simulation", simulation.shape)
        if plot == 'y':
            plt.plot(self.t_axis_4simu, simulation)
        return simulation


    def SpecRepsentation2(self, Sww, t_bins, freqs, plot='y'):
        """
        Note
        ----

        From an estimated evolutionary spectra, do simulation.
        a estimated EPSD with shape, e.g. (65, 41);

        Based on 'wu', 'N1' -> the freq axis
        Based on 'Fs', 'duration' -> the time axis
        ergo, we will interpolate a spectra with shape (N1, duration * Fs)

        Parameters
        -----------
        """

        # create the t axis
        n = np.arange(self.N1)
        delta_w = self.wu / self.N1
        w_n = n * delta_w
        A_n = np.sqrt(2 * Sww * delta_w)
        phi_n = np.random.uniform(0, 2 * np.pi, self.N1)

        # # Note that A0=0 or S(w0)=0
        # sum = 0
        # if Sww.shape[-1] == self.t_axis_4simu.shape[0]:
        #     for i in range(1, self.N1):
        #         sum = sum + A_n[i] * np.cos(w_n[i] * self.t_axis_4simu + phi_n[i])
        # elif Sww.shape[-1] < self.t_axis_4simu.shape[0]:
            # assert(t_bins != None)

        # Hint: we will construct a 2D grid

        ''' before: x -> t_axis
                    y -> w_axis
            eg. (65, 41)
        
            After: (N1, duration * Fs) -> (1024, 2500)
        '''


        # xx, yy = np.meshgrid(t_bins, freqs)
        # z = Sww
        # f = interpolate.interp2d(t_bins, freqs, z, 
        #                          kind='next', 
        #                          bounds_error=False, 
        #                          fill_value='extrapolate')

        # xnew = self.t_axis_4simu
        # ynew = self.w_axis_4simu
        # znew = f(xnew, ynew)
        
        points = np.meshgrid(t_bins, freqs)
        values = Sww
        grid_x, grid_y = np.mgrid[self.t_axis_4simu, self.w_axis_4simu]
        grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')

        return self.SpecRepsentation(grid_z0)





