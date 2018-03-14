import matplotlib
import matplotlib.pyplot as plt
import pandas
import sys
from matplotlib.backends.backend_pdf import PdfPages
matplotlib.rcParams['figure.figsize'] = (15, 8)
sys.path.append('/user/simon/development/soar/goodman')
from pipeline.core import SpectroscopicMode

spec_mode = SpectroscopicMode()


def process_grating(grating, df):
    print("")
    df = df[df.grating == grating]
    gdf = df.groupby(['grating', 'cam_targ', 'grt_targ']).size().reset_index().rename(columns={0: 'count'})
    modes = []
    count = []
    for i in gdf.index:
        mode = spec_mode(grating=grating,
                         camera_targ="{:.1f}".format(gdf.iloc[i]['cam_targ']),
                         grating_targ="{:.1f}".format(gdf.iloc[i]['grt_targ']))
        print("{:s} {:s} {:d} {:.1f} {:.1f}".format(grating,
                                                    mode,
                                                    gdf.iloc[i]['count'],
                                                    gdf.iloc[i]['cam_targ'],
                                                    gdf.iloc[i]['grt_targ']))
        if mode in modes:
            index = modes.index(mode)
            count[index] += gdf.iloc[i]['count']
        else:
            modes.append(mode)
            count.append(gdf.iloc[i]['count'])

    x_label = "Spectroscopic Modes"
    if not any([lmm in grating for lmm in ['1800', '2100', '2400']]):
        non_custom = []
        non_custom_count = []
        custom_count = 0
        for i in range(len(modes)):
            if 'Custom' in modes[i]:
                custom_count += count[i]
            else:
                non_custom.append(modes[i])
                non_custom_count.append(count[i])
        non_custom.append('Custom Modes')
        non_custom_count.append(custom_count)
        modes = non_custom
        count = non_custom_count
    else:
        x_label += " (Central Wavelength)"

    fig, ax = plt.subplots()
    title = "Goodman HTS \'\'Spectroscopic Modes\'\' used in 2017\nGrating: {:s}".format(grating)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Count")
    ax.tick_params(axis='x', rotation=70)
    ax.bar(range(len(modes)), count)
    ax.set_xticks(range(len(modes)))
    ax.set_xticklabels(modes)
    for i, tex in enumerate(count):
        ax.text(i, tex + 3, str(tex),
                 horizontalalignment='center',
                 fontweight='bold')
    plt.tight_layout()
    # plt.show()
    return fig

    # print(gdf)



file = 'goodman_modes.csv'

info = pandas.read_csv(file, names=['partner',
                                    'night',
                                    'grating',
                                    'cam_targ',
                                    'grt_targ'])
# filter out cam_targ == 0
# assume equal grating lines.
cleaned_info = info[(info['grating'] != "<NO GRATING>") &
                    (info['cam_targ'] != 0) &
                    (info['grt_targ'] != 0)]
# cleaned_info = info[info['cam_targ'] != 0]
# print(cleaned_info)
# print(info.grating)
# for grating in info.grating:
#     print(repr(grating))

grouped = cleaned_info.groupby(['grating', 'cam_targ', 'grt_targ']).size().reset_index().rename(columns={0: 'count'})
# print(grouped)
with PdfPages('all_lamps.pdf') as pdf:
    for grating in grouped.grating.unique():
        fig = process_grating(grating, cleaned_info)
        pdf.savefig(fig)
