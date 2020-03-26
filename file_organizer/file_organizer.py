"""main file for file organizer automation

Example:
    automation meant to be run on start up
        $ python example_google.py /home/frost/Documents/configs/file_config.xml


Attributes:
    config_location (str): String file path to the config file.  Writen in XML

Todo:
    * function: file tree scan
    * function: folder scanner
    * function: make folder
    * create config file
    * windows linux cross compatibility

"""

import shutil as sh
import xml.etree.ElementTree as et
import os
import sys


def move_file(old, new):
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
        print("[!] Error in move file")
        return 1


def is_dup(search_dir, file):
    """checks to see if file or folder exist within a given directory

        Parameters:
        search_dir (str): file path to search
        file (str): file to check inside the given folder

        Returns:
        int: 1 if the file or folder was found in the given directory, otherwise 0

       """

    with os.scandir(search_dir) as d:
        for item in d:
            if item.name == file:
                return 1
    return 0


def load_init_xml(config_location):
    """parses an xml config file into a dictionary variable

        Parameters:
        config_location (str): file path to config file

        Returns:
            a dictionary loaded with configurable options, returns 1 on error

       """

    try:
        root = et.parse(config_location).getroot().find("init")
        config = {"file_types": {}}

        for item in root:
            # loads all configs that do not have sub sections
            if not len(list(item)):
                config[item.tag] = item.text

        # loads the file structure and their file types
        struct_names = []
        for i, item in enumerate(root.find("file_structure"), start=1):
            file_names = []

            item_name = item.find('name').text
            struct_names.append(item_name)

            for j, subsec in enumerate(item):
                if subsec.tag == 'ext':
                    file_names.append(subsec.text)
            config["file_types"][item_name] = file_names
        struct_names.sort()
        config["file_structure"] = struct_names

        # loads in all directory paths to scan
        scan_dirs = []
        for i, item in enumerate(root.find("scan_dir"), start=1):
            scan_dirs.append(item.text)
        scan_dirs.sort()
        config["scan_dir"] = scan_dirs

        return config
    except:
        return 1


def main_logic():

    print("[#] main start")

    if len(sys.argv) != 2:
        print("[!] Usage: " + sys.argv[0] + " [config file]")
        return 1

    config = load_init_xml(sys.argv[1])

    if config == 1:
        print("[!] Error in config load")
        return 1

    return config


test = main_logic()

for thing in test:
    print(thing + ' --> ' + str(test[thing]))
