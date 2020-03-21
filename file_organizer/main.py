"""main file for file organizer automation

Example:
    automation meant to be run on start up
        $ python example_google.py /home/frost/Documents/configs/file_organizer.json


Attributes:
    config_location (str): String file path to the config file.  Writen in JSON

Todo:
    * function: rename file
    * function: is file a duplicate
    * function: load config
    * function: file tree scan
    * create config file

"""

import shutil as sh
import os


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


def rename_file(file_location, name):
    print("returns 0 if file was renamed correctly 1 on error")
    return 0


def is_dup(file_location):
    print("returns 1 if it is a dup otherwise a 0")
    return 0


def load_config(config_location):
    print("returns 0 if successful and 1 on error")
    return 0


def main_logic():
    old_path = "/home/frost/Documents/raw_docs/test.pdf"
    new_path = "/home/frost/Documents/raw_docs/pdf/test.pdf"

    print("[#] main start")

    print("[@] move_file test return: " + str(move_file(old_path, new_path)))


main_logic()
