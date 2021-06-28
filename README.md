# mwx-to-csv

Very simple script that extracts data from a Minitab worksheet into a more portable csv file.  
Requires numpy.

The data in .mwx worksheet files is stored using json, making Python a using tool for the job.

Example use: 

```sh
 python3 mwx_to_csv.py -i 'mydata.mwx' -o 'mydata.csv'
```