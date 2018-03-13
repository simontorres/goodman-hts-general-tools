import matplotlib
import matplotlib.pyplot as plt
import pandas

file = 'goodman_modes.csv'

info = pandas.read_csv(file, names=['partner',
                                    'night',
                                    'grating',
                                    'cam_targ',
                                    'grt_targ'])
# filter out cam_targ == 0
# assume equal grating lines.
print(info.groupby(['grating', 'cam_targ', 'grt_targ']).size().reset_index().rename(columns={0: 'count'}))