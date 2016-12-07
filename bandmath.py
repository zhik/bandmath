'''
notes
gdal_merge -co "PHOTOMETRIC=RGB" -separate 
https://github.com/dwtkns/gdal-cheat-sheet
http://www.perrygeo.com/running-python-with-compiled-code-on-aws-lambda.html
'''

# color = "res.txt"
# color = "dam.txt"
# color = "coffee.txt"
# color = "veg.txt"
color = "city.txt"

# Reservoir
# datasets = ["LC80430342016220LGN00","LC80430342016236LGN00", "LC80430342016252LGN00", "LC80430342016268LGN00", "LC80430342016300LGN00"]
# cropinput = "660096 4110621 687238 4085847"

# Wed May 01 2013 ,  Wed Aug 21 2013 , Sat Nov 09 2013 , Sat Nov 09 2013
# datasets = ["LC82220762013121LGN01","LC82220762013233LGN00","LC82220762013313LGN00"]
# cropinput = "479663 -2569429 518354 -2596971"

#japan 
datasets = ['LC81070352013260LGN00', 'LC81070352013324LGN00', 'LC81070352014087LGN00', 'LC81070352014151LGN00']
cropinput = "338493 3945182 356987 3925652"

gifName = "timelapse.gif"
gifDuration = 0.5


import os
#import gdal modules
import numpy as np
from osgeo import gdal
from gdalconst import *
from osgeo.gdalnumeric import *
#import gif modules
from images2gif import writeGif
from PIL import Image

#processes the tifs and runs bandmath on them
def processing_func():
    b = {}
    for band in bands:
        g = gdal.Open(dataset + "/" + dataset + "_" + band + clflag +".TIF", GA_ReadOnly)
        b[band] = np.array(g.ReadAsArray().astype(np.float))

    with np.errstate(divide='ignore', invalid='ignore'):
        # dataOut = np.nan_to_num(eval(bandmath, b))
        dataOut = eval(bandmath, b)

    #save file
    driver = gdal.GetDriverByName("GTiff")
    gOut = driver.Create(tifFile, g.RasterXSize, g.RasterYSize, 1, gdal.GDT_Float32)
    CopyDatasetInfo(g,gOut)
    bandOut= gOut.GetRasterBand(1)
    bandOut.WriteArray(dataOut)

    #close the datasets
    g = None
    for band in bands:
        band = None
    dataOut = None
    gOut = None
    bandOut = None

#gets a subset of the of the full tif
def crop(croparea):
    infile = dataset + "/" + dataset + "_" + band + ".TIF"
    outfile = dataset + "/" + dataset + "_" + band + clflag +".TIF"
    ulx, uly, lrx, lry = croparea[0], croparea[1], croparea[2], croparea[3]
    crop = "gdal_translate -projwin %s %s %s %s %s %s" %(ulx, uly, lrx, lry, infile, outfile)
    os.system(crop)


bandmath = raw_input("enter the band math: ")

#find the bands needed
bands = []
i = 0
while(True):
    p = bandmath.find("b",i) 
    if p != -1:
        band = bandmath[p:p+2]
        if bandmath[p:p+2] not in bands:
            bands.append(band)
        i += p + 1
        continue
    else:
        break

clflag = ""
print bands, bandmath #to debug
croparea = cropinput.split()

try:
    color
except NameError:
    color = "default.txt"
color = "color/"+ color

for dataset in datasets:
    for band in bands:
        if len(croparea) == 4:
            clflag = "c"
            crop(croparea)
    tifFile = dataset + ".tif"
    processing_func()
    imageFile = "jpeg/" + dataset + ".jpeg"
    covertimage = "gdaldem color-relief %s %s %s" %(tifFile, color, imageFile) #colors and exports as "jpeg"s
    os.system(covertimage)

#makes gifs
images = [Image.open("jpeg/"+fn+".jpeg") for fn in datasets]
for im in images:
    im.thumbnail(im.size)
writeGif(gifName, images, duration=gifDuration, subRectangles=False)

