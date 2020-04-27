"""main file for file organizer automation

Example:
    automation to be run on start up
        $ python example_google.py /home/frost/Documents/configs/file_config.xml


Attributes:
    config_location (str): String file path to the config file.  Writen in XML

"""

import shutil as sh
import xml.etree.ElementTree as et
import os
import sys
import time


def move(old, new):
    """File mover function

        Parameters:
            old (str): current file location
            new (str): destination file location

        Returns:
            int: 0 if move is successful and 1 on error

    """

    try:
        sh.move(old, new)

        return 0
    except:
        print('[!] Error in move file')
        return 1


def is_dup(search_dir, file):
    """checks to see if file or folder exist within a given directory

        Parameters:
            search_dir (str): file path to search
            file (str): file to check inside the given folder

        Returns:
            int: 1 if the file or folder was found in the given directory, otherwise 0

    """
    files = get_current(search_dir)[2]
    if len(files) and files.count(file):
        return 1
    return 0


def load_init_xml(config_location):
    """parses an xml config file into a dictionary variable

        Parameters:
            config_location (str): file path to config file

        Returns:
            a dictionary loaded with configurable options, returns 1 on error
            config = {'system':'', 'end_dir':'', 'file_types':{'item_name':[]}, 'file_structure':[], 'scan_dir':[]}

    """

    try:
        root = et.parse(config_location).getroot().find('init')
        config = {'file_types': {}}

        for item in root:
            # loads all configs that do not have sub sections
            if not len(list(item)):
                config[item.tag] = item.text

        # loads the file structure and their file types
        struct_names = []
        for i, item in enumerate(root.find('file_structure'), start=1):
            file_names = []

            item_name = item.find('name').text
            struct_names.append(item_name)

            for j, subsec in enumerate(item):
                if subsec.tag == 'ext':
                    file_names.append(subsec.text)
            config['file_types'][item_name] = file_names
        config['file_structure'] = struct_names
        config['file_structure'].sort()

        # loads in all directory paths to scan
        scan_dirs = []
        for i, item in enumerate(root.find('scan_dir'), start=1):
            scan_dirs.append(item.text)
        config['scan_dir'] = scan_dirs

        return config
    except:
        return 1


def get_current(to_scan):
    """takes a snapshot of the directory passed to it using os.walk()

        Parameters:
            to_scan (str): file path of the directory to be scanned

        Returns:
            a list representing the topmost level of the given directory
            current = [[path], [folders], [files]].

    """

    return next(os.walk(to_scan))


def check_folder_structure(config_st, to_scan):
    """generates a list of folders that needs to be added and or removed to be in line with the first parameter

        Parameters:
            config_st (list[str]): a list of folders to compare the current directory with
            to_scan (str): file path of the directory to be scanned

        Returns:
            a dictionary containing two lists of folder names
            {'add':[], 'remove':[], 'path':''}

    """

    current = get_current(to_scan)

    return {'add': list(set(config_st) - set(current[1])),
            'remove': list(set(current[1]) - set(config_st)),
            'path': current[0]}


def check_for_files(to_scan, file_type=None):
    """generates a list of files matching the file_type extension in the to_scan folder.

        if file_type is None this function will return all files within the to_scan folder.

        Parameters:
            to_scan (str): the file path to the folder that is to be scanned for the passed file_type.
            file_type (str): the file extension without the period to search the file for. Defaults to None.

        Returns:
            list: a list of files matching the provided file type or all the files in the folder if None is provided.

    """

    current = get_current(to_scan)[2]

    if file_type is not None:
        searched_files = current.copy()
        for file in current:
            if not file.endswith(file_type):
                searched_files.remove(file)
        return searched_files
    return current


def folder_logic(folders):
    print('[$] folder logic')

    for folder in folders['remove']:
        if os.stat(folder):
            file_logic(folder, )

    return 0


def file_logic(folder_from, folder_to):
    print('[$] file logic')
    pass


def organizer_logic_start(config_file='file_config.xml'):

    fin = True

    config = load_init_xml(config_file)

    if config == 1:
        print('[!] Error in config load', file=sys.stderr)
        sys.exit(1)

    while fin:

        root_folders = check_folder_structure(config['file_structure'], config['end_dir'])
        root_files = check_for_files(config['end_dir'])

        fin = False

        if len(root_folders['add']) or len(root_folders['remove']):
            folder_logic()
        if len(root_files):
            file_logic()

        # scan each scan_dir
            # if files found call function to move file to correct folder

        time.sleep(int(config['sleep_time']))

    print('[#] main loop end')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('[!] Usage: ' + sys.argv[0] + ' [config file]', file=sys.stderr)
        sys.exit(1)

    organizer_logic_start(sys.argv[1])
