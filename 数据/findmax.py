# 生成最大水深的文件

import os
import numpy as np
from osgeo import gdal
import pandas as pd


def to_raster(array,filepath):
    df = pd.DataFrame(array)
    with open(filepath, 'w+') as f:
        f.writelines('ncols         694\n')
        f.writelines('nrows         824\n')
        f.writelines('xllcorner     581104.93980083\n')
        f.writelines('yllcorner     3495917.0924138\n')
        f.writelines('cellsize      2\n')
        f.writelines('NODATA_value  -9999\n')
        f.close()
    df.to_csv(filepath, sep=' ', columns=None, index=False, header=False, mode='a+',float_format='%.3f')


i =gdal.Open('./LID_VS_10y/LID_VS_res/LID_VS_1-0001.wd').ReadAsArray()

for f in os.listdir('./LID_VS_10y/LID_VS_res'):
    if f[-3:]=='.wd':
        temp =  gdal.Open('./LID_VS_10y/LID_VS_res/'+f).ReadAsArray()
        i = np.dstack((i,temp))
    else:
        pass

maxdepth = np.max(i, axis=2)
to_raster(maxdepth,'./LID_analysis/LID_maxfile/LID_VS2_10y.txt')

