import argparse
import os
import re
import xlrd 
from xlrd.sheet import ctype_text 
from os.path import join, dirname, abspath
import re
from os.path import expanduser
import sys

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input', metavar='Excel File', type=str,
                     help='the Excel input file')
args = parser.parse_args()

def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)

    return s

fname = args.input
#fname = join(dirname(dirname(abspath(__file__))), 'amazon_polly', 'textDataset.xlsx')
xl_workbook = xlrd.open_workbook(fname)
xl_sheet = xl_workbook.sheet_by_index(0)
numOfRows = xl_sheet.nrows - 1
home = expanduser("~")
folderPath = home + "/" + "textfaPolly"
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

for rows in range(0, numOfRows):
    txt = xl_sheet.cell_value(rows, 0)
    filename  = urlify(txt) + ".txt"
    desPath = folderPath + "/" + filename
    with open(desPath, 'w+') as my_file:
        my_file.write(xl_sheet.cell_value(rows, 0))

exit(folderPath) 
