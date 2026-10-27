#!/usr/bin/env python3
"""Google Earth Engine (GEE) script template for extracting 1km MAIAC AOD & Sentinel-5P UVAI over Singapore."""

GEE_SCRIPT_TEMPLATE = '''
import ee
ee.Initialize()

sg_bbox = ee.Geometry.Rectangle([103.58, 1.15, 104.12, 1.48])
maiac = ee.ImageCollection("MODIS/061/MCD19A2_GRANULES") \
    .select("Optical_Depth_055") \
    .filterBounds(sg_bbox) \
    .filterDate("2015-09-01", "2015-10-31") \
    .mean()
'''
if __name__ == "__main__":
    print("GEE MAIAC 1km AOD template ready.")
