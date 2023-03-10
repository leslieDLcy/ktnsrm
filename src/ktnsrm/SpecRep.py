import numpy as np
import matplotlib.pyplot as plt

class SpecRep():

    def __init__(self, wg, zzeta, S0):
        """ initial the three parameter that define a KT model """ 

        self.wg = wg
        self.zzeta = zzeta
        self.S0 = S0


    def getKTspectrum(self, w):
        self._psd = self.S0 * (self.wg**4 + 4*(self.zzeta**2)*(self.wg**2)*(w**2)) / (((self.wg**2-w**2)**2) + 4*(self.zzeta**2)*(self.wg**2)*(w**2)) 


    @property
    def getPSD(self,):
        return self._psd



    #### time modulating function #####
    @staticmethod
    def envelop_tfunc1(t, b=4, c=0.8):
        """ set up a modulating function (from Liam 2015) """

        return b * (np.exp(-c * t) - np.exp(-2 * c * t))



    def sepEpsd(self, envelopfuncObj, t_axis):
        """ create a separable evolutionary spectum 
        
        Hint
        ----
        modulating_obj @ stationary_PSD


        Parameters
        ----------
        g(t)^2:
            the time modulating function;
        S(w):
            the stationary spectrm;
        """

        gt = envelopfuncObj(t_axis)
        gt2 = gt**2

        self._sepEPSD = np.outer(self._psd, gt2)
        print(r"the shape of the nonstationary spectra $S_{wt}$:", self._sepEPSD.shape)



    @staticmethod
    def nonsepEpsd(w_axis, t_axis):
        """ create a non-separable evollutionary spectrum 
        
        Parameters
        ----------        
        
        Hint
        ----
        Equation given in Liam 2015
        """


        a_list = []

        for w in w_axis:
            middleman = (w ** 2 / (5 * np.pi)) * np.exp(-0.15 * t_axis) * (t_axis ** 2) * np.exp( - ((w/(5 *np.pi)) ** 2) * t_axis)
            a_list.append(middleman)

        a_list = np.vstack(a_list)
        return a_list


    ##### displaying EPSD 2D/3D #####
    @staticmethod
    def EPSD_display(Pxx, freqs, t_bins, format, title_name='the estimated spectra'):
        """Given the 3 elements returned by plt.specgram
        
        Note
        ----
        To Compensate as one-sided plot


        ie, (Pxx, freqs, t_bins)
        ----
        Change the colorbar
        """

        if format=='2d':
            # hint: pcolormesh(t, f, EPSD)
            plt.pcolormesh(t_bins, freqs, Pxx, 
                    vmin=0, 
                    vmax=np.max(Pxx), 
                    shading='nearest', 
                    cmap='BuPu')
            plt.colorbar()
            plt.ylim([0, 100])
            plt.xlabel('Time (s)')
            plt.ylabel('Freq (rad)')
            plt.title(f'{title_name}')
        elif format=='3d':
            fig = plt.figure(figsize=(8, 6))    
            ax = plt.axes(projection='3d')
            X, Y = np.meshgrid(t_bins, freqs)
            Z = Pxx
            ax.plot_surface(X, Y, Z, cmap='BuGn')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (rad)')
            ax.set_zlabel('PSD')
            ax.set_title(f'{title_name}')





