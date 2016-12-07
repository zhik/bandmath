#for bandmath on latsat data
for GTECH 203 fall 2016 at Hunter College , [slides](https://github.com/zhik/bandmath/raw/master/slides.pdf)

code adapted from [geoxamples](http://geoexamples.blogspot.com/2012/12/raster-calculations-with-gdal-and-numpy.html)


- [x] bandmath script
- [x] get landsat data from aws script
- [ ] fix colors 
- [ ] add text to gifs

libraries used:
* gdal(osgeo4w)
* numpy
* images2gif

## bandmath.py 
**inscript setup** : color , datasets , cropinput , gifName , gifDuration

**input** : bandmath

**output** : bandmath-ed crop tiffs and colored jpegs , exported gif

## getbands.py 
**input** : pathrow , bands , ids (enter to finsh)

**output** : band tiffs in folders

##examples
![colorless](https://github.com/zhik/bandmath/raw/master/examples/colorless.gif)
![farm](https://github.com/zhik/bandmath/raw/master/examples/farm.gif)
