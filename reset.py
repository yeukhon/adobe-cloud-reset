#!/usr/bin/env python

import glob
import os
import re
import shutil

SL_DIRECTORIES = [
    '/Library/Application Support/Adobe/SLCache',
    '/Library/Application Support/Adobe/SLStore'
]

def extract_serial(line):
    pattern = '<Data key="TrialSerialNumber">(?P<serial>\d+)</Data>'
    r = re.compile(pattern)
    _line = line.strip()
    serial = r.match(_line).group('serial')
    int_serial = int(serial)
    return int_serial

def get_app_files():
    '''An iterator that returns the next Adobe application.xml to reset.'''

    for directory in glob.glob('/Library/Application Support/Adobe/Adobe *'):
        yield os.path.join(directory, 'AMT/application.xml')

def reset_trial():
    for app_file in get_app_files():
        file_content = []
        try:
            with open(app_file, 'r') as f:
                for line in f.readlines():
                    if 'TrialSerialNumber' in line:
                        curr_serial = extract_serial(line)
                        new_serial = str(curr_serial + 1)
                        new_serial_line = '<Data key="TrialSerialNumber">{serial}</Data>\n'.format(serial=new_serial)
                        file_content.append(new_serial_line)
                    else:
                        file_content.append(line)
            with open(app_file, 'w') as f:
                f.writelines(file_content)
        except IOError as e:
            print(e)

    # finish off by removing some cache files
    for path in SL_DIRECTORIES:
        try:
            shutil.rmtree(path)
        except OSError as e:
            print(e)
if __name__ == '__main__':
    reset_trial()
