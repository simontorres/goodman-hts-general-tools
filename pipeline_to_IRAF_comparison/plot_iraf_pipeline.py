import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np
import scipy.interpolate
from scipy import signal
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes,\
    mark_inset, inset_axes

from ccdproc import CCDData
from goodman_spec.wsbuilder import ReadWavelengthSolution

offset = 8000.

iraf_file = '/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/CVSO-114SW_400M2_comb_1d_wl.fits'
pipe_file = '/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/gcfzsto_0074.cvso114_400M2_GG455_1.fits'

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

new_x_axis = np.linspace(wav_min, wav_max, 2 * len(iraf_w))

iraf_new_w_axis = np.linspace(iraf_w[0], iraf_w[-1], 2 * len(iraf_w))
iraf_tck = scipy.interpolate.splrep(iraf_w, iraf_i, s=0)
iraf_interp = scipy.interpolate.splev(new_x_axis, iraf_tck, der=0)

pipe_new_w_axis = np.linspace(pipe_w[0], pipe_w[-1], 2 * len(pipe_w))
pipe_tck = scipy.interpolate.splrep(pipe_w, pipe_i, s=0)
pipe_interp = scipy.interpolate.splev(new_x_axis, pipe_tck, der=0)

pipe_interp[pipe_interp < 0] = 0
iraf_interp[iraf_interp < 0] = 0

difference = pipe_interp - iraf_interp

lowlim = max([iraf_new_w_axis[0], pipe_new_w_axis[0]])

# plt.xlim((wav_min, wav_max))
#
# plt.plot(new_x_axis, iraf_interp, color='r')
# plt.plot(new_x_axis, pipe_interp, color='k')
# plt.plot(new_x_axis, difference, color='m')
# plt.show()

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

plt.xlim((wav_min, wav_max))

ax.axvline(6562.8, color='k', linestyle='--', alpha=0.3, label=r'$H\alpha$ 6562.8 $\AA$')
ax.plot(iraf_w, iraf_oi, label='IRAF Solved + Offset', color='#7688A9')
ax.plot(pipe_w, pipe_i, label='Goodman Pipeline', color='#051838')
ax.set_title('Pipeline V/S IRAF comparison\nCVSO-114\n400M2 + GG455')
ax.set_xlabel('Wavelength (Angstrom)')
ax.set_ylabel('Intensity (ADU)')
ax.legend(loc='best')
fig.tight_layout()

# sub_plot =

# axins = zoomed_inset_axes(ax, 2, loc=1)
axins = inset_axes(ax, width="28%", height=2., loc=4)
axins.axvline(6562.8, color='k', linestyle='--', alpha=0.3, label=r'H-alpha 6562.8\AA')
axins.plot(iraf_w, iraf_oi, label='IRAF Solved + Offset', color='#7688A9')
axins.plot(pipe_w, pipe_i, label='Goodman Pipeline', color='#051838')

axins.set_xlim(6480, 6620)
axins.set_ylim(9950, 23550)
plt.xticks(visible=False)
plt.yticks(visible=False)

mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.5")

plt.savefig('/data/simon/development/soar/goodman-hts-general-tools/pipeline_to_IRAF_comparison/files/pipe_iraf_corrected.png', dpi=300)
plt.show()