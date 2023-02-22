# 把研究区域外的栅格水深结果从0改为-9999

from osgeo import gdal
import pandas as pd

def setnull(array,template):
    rows = 824
    cols = 694
    for i in range(rows):
        for j in range(cols):
            if template[i][j] == -9999:
                array[i][j] = -9999

def to_asc(array,filepath):
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


# damage = gdal.Open('./damage_function/damage_10y.txt').ReadAsArray()
# landuse = gdal.Open('./landuse.txt').ReadAsArray()
# setnull(damage,landuse)
# to_asc(damage,'./damage_function/damage_null/dam_null_10y.txt')