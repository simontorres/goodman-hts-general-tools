import matplotlib.pyplot as plt
import astropy.units as u
from ccdproc import CCDData
from goodman_spec.wsbuilder import ReadWavelengthSolution

offset = 6000.

iraf_file = '/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/CVSO-114SW_400M2_comb_1d_wl.fits'
pipe_file = '/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/auto_gcfzsto_0074.cvso114_400M2_GG455_1.fits'

iraf_data = CCDData.read(iraf_file, unit=u.adu)

iraf_ws = ReadWavelengthSolution(header=iraf_data.header,
                                 data=iraf_data.data)

pipe_data = CCDData.read(pipe_file, unit=u.adu)

pipe_ws = ReadWavelengthSolution(header=pipe_data.header,
                                 data=pipe_data.data)


iraf_w, iraf_i = iraf_ws()

iraf_oi = iraf_i + offset

pipe_w, pipe_i = pipe_ws()

wav_min = min([iraf_w[0], pipe_w[0]])

wav_max = max([iraf_w[-1], pipe_w[-1]])
print(wav_min, wav_max)

plt.xlim((wav_min, wav_max))

plt.axvline(6562.8, color='r', label='H-alpha 6562.8A')
plt.plot(iraf_w, iraf_oi, label='IRAF Solved + Offset', color='k', alpha=.5)
plt.plot(pipe_w, pipe_i, label='Goodman Pipeline', color='k')
plt.title('Pipeline V/S IRAF comparison\nCVSO-114\n400M2 + GG455')
plt.xlabel('Wavelength (Angstrom)')
plt.ylabel('Intensity (ADU)')
plt.legend(loc='best')
plt.tight_layout()

plt.savefig('/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/pipe_iraf.png', dpi=300)
plt.show()