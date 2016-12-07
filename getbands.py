#https://remotepixel.ca/projects/satellitesearch.html

import urllib
import os
import sys
from time import sleep

#from http://stackoverflow.com/questions/51212/how-to-write-a-download-progress-indicator-in-python
def dlProgress(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    sys.stdout.write("\r%2d%% %s %s" %(percent, band, id))
    sys.stdout.flush()

baseurl = "http://landsat-pds.s3.amazonaws.com/L8/"
pathrow = raw_input("enter path/row: ")
bands = raw_input("enter bands: ").upper()

bands = bands.split()
ids = []

while True:
    id = raw_input("enter ids: ")
    if id == "":
        break
    ids.append(id)

for id in ids:
    if not os.path.exists(id):
        os.makedirs(id)
    for band in bands:
        filename =  id + "/" + id + "_" + band + ".TIF"
        url = baseurl + pathrow + "/" + filename
        urllib.urlretrieve(url, filename, reporthook=dlProgress)
        sleep(.1)

print "\n" , ids
