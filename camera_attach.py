import time
import subprocess

while True:
    output = subprocess.run('usbipd list', capture_output=True, encoding="UTF-8")
    rows = output.stdout.split('\n')
    for row in rows:
        if ('Movidius MyriadX' in row or 'Luxonis Device' in row) and 'Not shared' in row:
            busid = row.split(' ')[0]
            out = subprocess.run(f'usbipd bind -b {busid}', capture_output=True, encoding="UTF-8")
            print(out.stdout)
            print(f'Usbipd bind Myriad X')
        if ('Movidius MyriadX' in row or 'Luxonis Device' in row) and 'Shared' in row:
            busid = row.split(' ')[0]
            out = subprocess.run(f'usbipd attach -w -b {busid}', capture_output=True, encoding="UTF-8")
            print(out.stdout)
            print(f'Usbipd attached Myriad X on bus {busid}')
    time.sleep(0.5)