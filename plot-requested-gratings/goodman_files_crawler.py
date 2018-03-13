import glob
import os
import subprocess

# data_location = '/SPARTAN/GOODMAN_DATA'
data_location = '/home/observer/GOODMAN_DATA'
partner = ['NOAO', 'CHILE', 'MSU', 'UNC', 'BRAZIL', 'OTHER']

for part in partner:
    partner_path = os.path.join(data_location, part)
    if os.path.isdir(partner_path):
        directories = glob.glob(os.path.join(partner_path, '2017*/*fits'))
        for files in directories:
            command = "gethead %s grating cam_targ grt_targ" % (files)
            # print(command.split())
            try:
                subp = subprocess.Popen(command.split(),
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
            except OSError:
                print("error")
            # print(command)
            def kill_process(process):
                process.kill()

            stdout, stderr = subp.communicate()
            print("%s, %s" % (', '.join(files.split('/')[4:6]), ', '.join(stdout.split())))
    else:
        print("Partner Folder Does not exists: %s" %(partner_path))