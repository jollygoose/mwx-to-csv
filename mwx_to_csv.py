#!/usr/bin/env python3

"""Extracts data from a Minitab worksheet into a more portable csv file. Requires numpy.

The data in worksheet files is stored in json format so Python's json library is great
for the job.

Example use: 

>>> python3 mwx_to_csv.py -i 'mydata.mwx' -o 'mydata.csv'

"""


import argparse
from zipfile import ZipFile
import json
import csv
import numpy


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', dest="input_file",
                help="Location of the Minitab file (.mwx)")
ap.add_argument('-o', '--output', dest="output_file",
                help="Name of the resulting csv file")
args = ap.parse_args()

csv_data = []

with ZipFile(args.input_file) as zipfile:
    # the json data containing the worksheet data is locating in the /sheets/0/ directory
    with zipfile.open('/sheets/0/sheet.json') as mwxfile:

        # read in the binary data and decode to text
        data_raw = mwxfile.read().decode('utf-8')

        # the number of data columns can be tallied by counting the 'WorksheetVarBody' keys. The key index
        # is used for building the key sequences when reading the JSON data
        num_cols = data_raw.count('WorksheetVarBody')

        data = json.loads(data_raw)

        for i in range(num_cols):
            column_data = []
            column_data.append(
                data['Data']['Columns'][i]['WorksheetVarBody']['Name'])
            # treat as numeric data by default, and swap to text data when needed
            try:
                column_data.extend(
                    data['Data']['Columns'][i]['WorksheetVarBody']['VarData']['VarDataBody']['NumericData'])
            except KeyError:
                column_data.extend(
                    data['Data']['Columns'][i]['WorksheetVarBody']['VarData']['VarDataBody']['TextData'])
            csv_data.append(column_data)

    # convert rows to columns
    csv_data = numpy.transpose(csv_data)

    with open(args.output_file, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerows(csv_data)
