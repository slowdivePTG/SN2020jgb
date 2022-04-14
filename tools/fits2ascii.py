from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def fits2ascii(file, output, lower=-np.inf, upper=np.inf):
    sn = fits.open(file)
    header = (sn[0].header + sn[1].header).tostring(sep="\n", endcard=False,padding=False)
    wv = sn[1].data["wave"]
    fl = sn[1].data['flux']
    unc = sn[1].data["ivar"] ** -0.5
    fl = fl[(wv > lower) & (wv < upper)]
    unc = unc[(wv > lower) & (wv < upper)]
    wv = wv[(wv > lower) & (wv < upper)]
    np.savetxt(
          output,
          np.array([wv, fl, unc]).T,
          fmt=("%.4f", "%.4f", "%.4e"),
          header=header,
      )
    plt.errorbar(wv, fl/np.nanmedian(fl), yerr=unc)
    plt.errorbar(wv, fl/unc, color='k')
    plt.show()
