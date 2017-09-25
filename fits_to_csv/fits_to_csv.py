from ccdproc import CCDData
from astropy import units as u
from goodman_spec.wsbuilder import ReadWavelengthSolution

import csv
from itertools import izip

fits_file = 'auto_gcfzsto_0074.cvso114_400M2_GG455_1.fits'

ccd = CCDData.read(fits_file, unit=u.adu)

read_ws = ReadWavelengthSolution(header=ccd.header,
                                 data=ccd.data)

wave, intens = read_ws()

with open('spectrum.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(wave, intens))


