import matplotlib.pyplot as plt 
import numpy as np
import itertools
import pandas as pd
from matplotlib import mlab
from scipy.interpolate import griddata

def EPSD_show(Pxx, freqs, t_bins, format, title_name='the estimated spectra'):
        """Given the 3 elements returned by plt.specgram
        ie, (Pxx, freqs, t_bins)
        ----
        Change the colorbar
        """
        plt.figure(figsize=(6,4))
        if format=='2d':
            plt.pcolormesh(t_bins, freqs, Pxx, 
                    vmin=0, 
                    vmax=np.max(Pxx), 
                    shading='nearest', 
                    cmap='GnBu')
            plt.colorbar()
            plt.ylim([0, 15])
            plt.xlabel('time (s)')
            plt.ylabel('freq (HZ)')
            # plt.grid()
            plt.title(f'{title_name}')
        elif format=='3d':
            fig = plt.figure(figsize=(8,8))    
            ax = plt.axes(projection='3d')
            X, Y = np.meshgrid(t_bins, freqs)
            Z = Pxx
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel('time (s)')
            ax.set_ylabel('frequency (hz)')
            ax.set_zlabel('PSD')
            ax.set_title(f'{title_name}')


def specgram3d(y, fs=200, title=None):
        """
        This func is borrowed elsewhere
        """
        ax = plt.axes(projection='3d')
        ax.set_title(title, loc='center', wrap=True)
        spec, freqs, t = mlab.specgram(y, Fs=fs, NFFT=256, noverlap=128)
        X, Y, Z = t[None, :], freqs[:, None], spec
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xlabel('time (s)')
        ax.set_ylabel('frequencies (Hz)')
        ax.set_zlabel('PSD')
#         ax.set_zlim([0, 0.015])
#         ax.set_ylim([0, 10])
#         ax.set_xlim([0, 14])
#         ax.view_init(20, 220)
        ax.invert_xaxis()
#         ax.invert_yaxis()
        return X, Y, Z


def simple_interpol2d(Pxx, freqs, t_bins):
    """Since the shape of estimated Swt spectra is smaller than 
    the one used to do SRM simulation, we interpolate it.
    TODO:
    -----
    The Swt should be interpolated to a given shape by (N1, duration * Fs)
    """
    # Use the same variables names as the Numpy example
    # Points, values, and then new coordinates
    points = list(itertools.product(t_bins, freqs))
    
    sample_df = pd.DataFrame()
    sample_df['X'] = [xy[0] for xy in points]
    sample_df['Y'] = [xy[1] for xy in points]
    # sample_df['value'] = values

    up_reversed = np.flipud(Pxx)
    values = np.ravel(up_reversed, order='F')

    x_min, x_max = 0.0, sample_df['X'].max()
    y_min, y_max = 0.0, sample_df['Y'].max()

    new_x_coord = np.linspace(x_min, x_max, 2500)
    new_y_coord = np.linspace(y_min, y_max, 1024)
    xx, yy = np.meshgrid(new_x_coord, new_y_coord)
    grid_z0 = griddata(points, values, xi=(xx, yy), method='nearest')
    print("double check the shape after interpolation:", grid_z0.shape)
    return grid_z0
