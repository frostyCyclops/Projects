'''

temporary file just so I can step through code using Pycharm's debugger.
there is a bug with 'import xml.etree.ElementTree as et' and the debugger
that will crash unless the import is removed, ie loading the config file

'''

import os


def get_current(to_scan):
    """takes a snapshot of the directory passed to it using os.walk()

        Parameters:
        to_scan (str): file path of the directory to be scanned

        Returns:
            a list representing the topmost level of the given directory
            current = [[path], [folders], [files]].

    """

    return next(os.walk(to_scan))


def check_for_files(to_scan, file_type=None):

    current = get_current(to_scan)[2]
    searched_files = current.copy()

    if file_type is not None:
        for file in current:
            if not file.endswith(file_type):
                searched_files.remove(file)
        return searched_files
    return current


end_dir = '/home/frost/Documents/raw_docs'
type_file = 'txt'

print('')
print(check_for_files(end_dir, type_file))
