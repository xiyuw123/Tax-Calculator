import cPickle

# needed for modifying the CSV
import pandas as pd
import numpy as np


def pickle_puf(input_filename, output_filename, protocol=2):
    '''Given a name for input and output files, opens input (assumes it's CSV)
    file and pickles it using the protocol (can be optionally set to 0 or 1,
    see docs for cPickle) with the output file name.
    '''
    csv_dataframe = pd.read_csv(input_filename)
    # this code is specific to OSPC processing of the CSV
    # narray_dict = {'PUF DIM': len(csv_dataframe)}
    # We save the length of the PUF table for processing in calc
    for col_name in csv_dataframe.columns.values:
        new_col = col_name.upper() if col_name.isalpha() else col_name
        narray_dict[new_col] = np.array(csv_dataframe[col_name])

    with open(output_filename, 'w') as target:
        cPickle.dump(narray_dict, target, protocol)


def unpicle(f_name):
    '''Given a file name opens the file and uses cPickle to load it as a python
    object.
    '''
    with open(f_name) as y_file:
        return cPickle.load(y_file)


import csv
from collections import defaultdict

def pickle_c_codes(f_name, output_filename):
    '''Function to pickle a C-code csv file.
    Because the C-code file is so large, we have to incrementally read it in,
    then turn every variable into an np.array, then pickle the result.

    We should consider alternatives like memory map and PyTables.
    '''
    with open(f_name) as c_file:
        d = csv.DictReader(c_file)
        acrue = defaultdict(list)
        for row in d:
            for key in row:
                acrue[key].append(row[key])

    with open(output_filename, 'w') as out_file:
        cPickle.dump(acrue, out_file, protocol=2)


if __name__ == '__main__':
    # pickle_c_codes('withc.csv', 'withc.pickle')
    pass
