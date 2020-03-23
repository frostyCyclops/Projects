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
    """loads the configuration file for the script and sets root to init

        Parameters:
        config_location (str): file path to config file

        Returns:
            an element tree at init if successful, returns 1 on error

       """

    try:
        return et.parse(config_location).getroot().find("init")
    except:
        return 1


def main_logic():

    print("[#] main start")

    if len(sys.argv) != 2:
        print("[!] Usage: " + sys.argv[0] + " [config file]")
        return 1

    config_init = load_init_xml(sys.argv[1])

    if config_init == 1:
        print("[!] Error in config load")
        return 1

    system = config_init.find("system").text
    start_dir = config_init.find("start_dir").text

    file_to_check = "pdf"

    # print("[#] move_file test return: " + str(move_file(old_path, new_path)))
    print("[#] is_dup test return: " + str(is_dup(start_dir, file_to_check)))


main_logic()
