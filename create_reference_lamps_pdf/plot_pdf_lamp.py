import argparse
import astropy.units as u
from ccdproc import CCDData
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy import signal


from goodman_spec.wsbuilder import ReadWavelengthSolution
from goodman_spec.linelist import ReferenceData
from goodman_spec.wavelength import WavelengthCalibration




def get_args(arguments=None):
    parser = argparse.ArgumentParser(description="Plot reference lamps trying"
                                                 "to mark the lines.")

    parser.add_argument('--lamp',
                        action='store',
                        type=str,
                        dest='lamp_name',
                        help='The lamp to be plotted.')

    parser.add_argument('--reference-dir',
                        default='/data/simon/development/soar/goodman/goodman/data/ref_comp',
                        dest='reference_dir')

    args = parser.parse_args(args=arguments)

    return args


def get_lines_in_lamp(ccd=None):
    """Identify peaks in a lamp spectrum

    Uses scipy.signal.argrelmax to find peaks in a spectrum i.e emission
    lines, then it calls the recenter_lines method that will recenter them
    using a "center of mass", because, not always the maximum value (peak)
    is the center of the line.

    Returns:
        lines_candidates (list): A common list containing pixel values at
            approximate location of lines.

    """

    # if ccd is None:
    #     lamp_data = self.lamp_data
    #     lamp_header = self.lamp_header
    #     raw_pixel_axis = self.raw_pixel_axis
    assert isinstance(ccd, CCDData)
    # print(ccd.data.shape)
    lamp_data = ccd.data
    lamp_header = ccd.header
    raw_pixel_axis = range(len(lamp_data))


    no_nan_lamp_data = np.nan_to_num(lamp_data)

    filtered_data = np.where(
        np.abs(no_nan_lamp_data > no_nan_lamp_data.min() +
               0.03 * no_nan_lamp_data.max()),
        no_nan_lamp_data,
        None)

    # plt.plot(filtered_data)
    # plt.show()

    _upper_limit = no_nan_lamp_data.min() + 0.03 * no_nan_lamp_data.max()
    slit_size = re.sub('[a-zA-Z" ]', '', lamp_header['slit'])

    serial_binning, parallel_binning = [
        int(x) for x in lamp_header['CCDSUM'].split()]

    new_order = int(round(float(slit_size) / (0.15 * serial_binning)))
    # log.debug('New Order:  {:d}'.format(new_order))

    print(round(new_order))
    peaks = signal.argrelmax(filtered_data, axis=0, order=new_order)[0]

    # if slit_size >= 5:
    #
    #     lines_center = self.recenter_broad_lines(lamp_data=no_nan_lamp_data,
    #                                              lines=peaks,
    #                                              order=new_order)
    # else:
    #     # lines_center = peaks
    #     lines_center = self.recenter_lines(no_nan_lamp_data, peaks)

    if True:
        fig = plt.figure(1)
        fig.canvas.set_window_title('Lines Detected')
        plt.title('Lines detected in Lamp\n{:s}'.format(lamp_header['OBJECT']))
        plt.xlabel('Pixel Axis')
        plt.ylabel('Intensity (counts)')

        # Build legends without data to avoid repetitions
        plt.plot([], color='k', label='Comparison Lamp Data')
        plt.plot([], color='k', linestyle=':', label='Spectral Line Detected')
        plt.axhline(_upper_limit, color='r')

        for line in peaks:
            plt.axvline(line + 1, color='k', linestyle=':')

        # plt.axhline(median + stddev, color='g')
        # for rc_line in lines_center:
        #     plt.axvline(rc_line, color='r')

        plt.plot(raw_pixel_axis, no_nan_lamp_data, color='k')
        plt.legend(loc='best')
        plt.show()

    return peaks


def make_plot(lamp, args=None):
    assert lamp is not None
    ccd = CCDData.read(lamp, unit=u.adu)

    lines = get_lines_in_lamp(ccd=ccd)
    print(lines)

    wsolution = ReadWavelengthSolution(header=ccd.header, data=ccd.data)

    wave, intens = wsolution()

    refdata = ReferenceData(args)

    lines_in_range = refdata.get_lines_in_range(wave[0], wave[-1], ccd.header['OBJECT'].lower())

    print(lines_in_range)
    # from lines import cuhear
    #
    # lines_in_range = cuhear



    # ccd_lamp = CCDData.read('/data/simon/development/soar/goodman/goodman/data/ref_comp/goodman_comp_1200_M2_CuHeAr.fits', unit=u.adu)
    #
    # ws2 = ReadWavelengthSolution(header=ccd_lamp.header, data=ccd_lamp.data)
    #
    # w2, i2 = ws2()
    #
    # ll = []
    # for l in lines_in_range:
    #     if l > w2[0] and l < w2[-1]:
    #         ll.append(l)


    plt.plot(wave, intens, label='NOAO Lamp (web)')
    plt.plot([], color='k', alpha=0.3, label=r'Reference values $\AA$')
    for l in lines_in_range:
        plt.axvline(l, color='k', alpha=0.3)
    for k in wsolution.math_model(lines):
        plt.axvline(k, color='r')
    # plt.plot(w2, i2, color='m',  label='Ref Lamp (1200M3)')
    plt.legend(loc='best')
    plt.show()


if  __name__ == '__main__':
    args = get_args()
    make_plot(args.lamp_name, args)