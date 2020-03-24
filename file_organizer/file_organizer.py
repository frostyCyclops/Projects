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
        config = {"file_structure": {}, "file_types": {}, "scan_dir": {}}

        for item in root:
            # loads all configs that do not have sub sections
            if not len(list(item)):
                config[item.tag] = item.text

        # loads the file structure and their file types
        for i, item in enumerate(root.find("file_structure"), start=1):
            name = item.find('name').text
            config["file_structure"][i] = name

            config["file_types"][name] = {}
            for j, subsec in enumerate(item):
                if subsec.tag == 'ext':
                    config["file_types"][name][j] = subsec.text

        # loads in all directory paths to scan
        for i, item in enumerate(root.find("scan_dir"), start=1):
            config["scan_dir"][i] = item.text

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

    print("[#] config --> " + str(config))


main_logic()
