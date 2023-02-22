import pandas as pd
from osgeo import gdal
import numpy as np

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

# 防止超过最大值
def setmax(array,threshold):
    rows = 824
    cols = 694
    for i in range(rows):
        for j in range(cols):
            x = array[i][j]
            if x >= threshold:
                x = threshold

def totaldamage(array):
    box = []
    rows = 824
    cols = 694
    for i in range(rows):
        for j in range(cols):
            if array[i][j] > -9999:
                x = array[i][j]
                box.append(x)
    print(sum(box))

#
# landuse = gdal.Open('./landuse.txt').ReadAsArray()
# maxdepth = gdal.Open('./LID_analysis/LID_maxfile/LID_VS2_30y.txt').ReadAsArray()
# six type of landuse map
# resident = np.where(landuse==1, 1, 0)
# res_depth = maxdepth*resident
# #
# commerce = np.where(landuse==2, 1, 0)
# com_depth = maxdepth*commerce
#
# greenland = np.where(landuse==3, 1, 0)
# gre_depth = maxdepth*greenland
#
# road = np.where(landuse==4, 1, 0)
# road_depth = maxdepth*road
#
# public = np.where(landuse==5, 1, 0)
# pub_depth = maxdepth*public
#
# # water = np.where(landuse==6, 0, 0)
# rows, cols = landuse.shape
#
# # damage calculation
# # ---resident
# loss_res = res_depth*16.682*874.73*0.01
# loss_com = com_depth*6.8517*1372.12*0.01
# loss_roa = road_depth*4.4194*361.39*0.01
# loss_gre = gre_depth*36.304*179.14*0.01
# loss_pub = pub_depth*11.645*416.52*0.01
# setmax(loss_gre, 179.14)
# setmax(loss_roa, 361.79)


# loss_res = resones*874.73
# loss_com = com_ones*1372.12
# loss_roa = road_ones*361.39
# loss_gre = gre_ones*179.14
# loss_pub = pub_ones*416.52
# loss = loss_res+loss_roa+loss_com++loss_gre+loss_pub
#
# to_raster(loss,'./LID_analysis/LID_damage/LID_VS2_30y.txt')


array = gdal.Open('./LID_analysis/LID_damage/Base_50y.txt').ReadAsArray()
totaldamage(array)