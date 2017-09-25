import matplotlib.pyplot as plt
import astropy.units as u
from ccdproc import CCDData
from goodman_spec.wsbuilder import ReadWavelengthSolution


iraf_file = './files/CVSO-114SW_400M2_comb_1d_wl.fits'
pipe_file = './files/auto_gcfzsto_0074.cvso114_400M2_GG455_1.fits'

iraf_data = CCDData.read(iraf_file, unit=u.adu)

iraf_ws = ReadWavelengthSolution(iraf_data.header, iraf_data.data)

pipe_data = CCDData.read(pipe_file, unit=u.adu)

pipe_ws = ReadWavelengthSolution(pipe_data.header, pipe_data.data)


iraf = iraf_ws()

pipe = pipe_ws()

wav_min = min([iraf[0][0], pipe[0][0]])

wav_max = max([iraf[0][-1], pipe[0][-1]])
print(wav_min, wav_max)

plt.xlim((wav_min, wav_max))

plt.plot(iraf[0], iraf[1], label='IRAF Solved', color='k', alpha=.7)
plt.plot(pipe[0], pipe[1], label='Goodman Pipeline', color='k')
plt.axvline(6562.8, color='r', label='H-alpha 6562.8A')
plt.legend(loc='best')
plt.show()