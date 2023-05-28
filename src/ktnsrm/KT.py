import numpy as np
import matplotlib.pyplot as plt

class KT():
    """ the base Kanai Tajimi model """

    def __init__(self, wg, zzeta, S0):
        """ initial the three parameter that define a KT model """ 

        self.wg = wg
        self.zzeta = zzeta
        self.S0 = S0


    def get_psd(self, w):
        self._KTpsd =  self.S0 * (self.wg**4 + 4*(self.zzeta**2)*(self.wg**2)*(w**2)) / (((self.wg**2-w**2)**2) + 4*(self.zzeta**2)*(self.wg**2)*(w**2)) 


    @property
    def PSD(self,):
        return self._KTpsd


    def plot_PSD(self, w_axis):
        """ plot the one-sided defined PSD """
        
        assert hasattr(self, '_KTpsd'), "run 'get_psd' first"

        fig, ax = plt.subplots()
        ax.plot(w_axis, self.PSD)
        ax.set_title("a parameterized Kanai Tajimi model")
        ax.set_xlabel(r'Frequency $w$ (rad/s)')
        ax.set_ylabel('Power spectral density')


    def cp_SepEpsd(self, envelopfuncObj, t_axis):
        """ create a separable evolutionary spectum with given envolop
        
        Hint
        ----
        modulating_obj @ stationary_PSD; implicitly create property `self._sepEPSD`


        Parameters
        ----------
        g(t)^2:
            the time modulating function;
        S(w):
            the stationary spectrm;
        """

        gt = envelopfuncObj(t_axis)
        gt2 = gt**2

        self._sepEPSD = np.outer(self.PSD, gt2)
        print("the shape of the nonstationary spectra" + r"$S_{wt}$", self._sepEPSD.shape)


    @staticmethod
    def cp_NonSepEpsd(w_axis, t_axis):
        """ A totally customized non-separable evolutionary spectrum 
        
        Parameters
        ----------        
        w_axis : array
            the frequency axis
        t_axis : array
            the time axis

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
    def EPSD_display(Pxx, freqs, t_bins, format, title_name='the defined evolutionary spectra'):
        """Given the 3 elements returned by plt.specgram
        
        Note
        ----
        To Compensate as one-sided plot

        ie, (Pxx, freqs, t_bins)
        ----
        Change the colorbar
        """

        if format=='2d':
            fig = plt.figure()
            # hint: pcolormesh(t, f, EPSD)
            plt.pcolormesh(t_bins, freqs, Pxx, 
                    vmin=0, 
                    vmax=np.max(Pxx), 
                    shading='nearest', 
                    cmap='BuPu')
            plt.colorbar()
            plt.ylim([0, 100])
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (rad/s)')
            plt.title(f'{title_name}')
        elif format=='3d':
            fig = plt.figure(figsize=(8, 8))    
            ax = plt.axes(projection='3d')
            X, Y = np.meshgrid(t_bins, freqs)
            Z = Pxx
            ax.plot_surface(X, Y, Z, cmap='bwr')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (rad/s)')
            ax.set_zlabel('PSD')
            ax.set_title(f'{title_name}')





