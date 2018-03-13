import re
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rcParams['figure.figsize'] = (16, 9)

file = '/data/simon/documentation/soar/general_documentation/goodman_gratings/gratings.txt'

to_find = ['400', '600', '930', '1200', '1800', '2100', '2400']
count = [0] * len(to_find)


with open(file) as grt:
    for line in grt.readlines():
        for i in range(len(to_find)):
            if len(re.findall(to_find[i], line)) > 0:
                count[i] += len(re.findall(to_find[i], line))
        print(line)

for i in range(len(to_find)):
    print(to_find[i], count[i])

pdf_file = 'requested-gratings-2017.pdf'
png_file = 'requested-gratings-2017.png'
with PdfPages(pdf_file) as pdff:

    plt.title('Gratings Requested During 2017\nGoodman High Throughput Spectrograph')
    plt.xlabel("Grating (lines/mm)")
    plt.ylabel("Count")
    plt.bar(range(len(to_find)), count)
    plt.xticks(range(len(to_find)), to_find)
    for i, v in enumerate(count):
        plt.text(i, v + 3, str(v), horizontalalignment='center', fontweight='bold')
    plt.tight_layout()
    pdff.savefig()
    plt.savefig(png_file, dpi=300)



    plt.show()