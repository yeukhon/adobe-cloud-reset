#!/usr/bin/env python

import glob
import os
import random

EXCLUDED_DIRS = [
    '/Library/Application Support/Adobe/Adobe Desktop Common',
    '/Library/Application Support/Adobe/Adobe PCD'
]

def random_serial():
    rand = random.SystemRandom()
    return ''.join(str(rand.randrange(9)) for i in range(24))

def get_app_files():
    '''An iterator that returns the next Adobe application.xml to reset.'''

    for directory in glob.glob('/Library/Application Support/Adobe/Adobe *'):
        if directory not in EXCLUDED_DIRS:
            yield os.path.join(directory, 'AMT/application.xml')

def reset_trial():
    for app_file in get_app_files():
        file_content = []
        try:
            with open(app_file, 'r') as f:
                print(app_file)
                for line in f.readlines():
                    if 'TrialSerialNumber' in line:
                        serial = random_serial()
                        new_serial_line = '<Data key="TrialSerialNumber">{serial}</Data>\n'.format(serial=serial)
                        file_content.append(new_serial_line)
                    else:
                        file_content.append(line)
            with open(app_file, 'w') as f:
                f.writelines(file_content)
        except IOError as e:
            print(e)

if __name__ == '__main__':
    reset_trial()
