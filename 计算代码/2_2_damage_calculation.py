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


landuse = gdal.Open('./计算代码/landuse.txt').ReadAsArray()
maxdepth = gdal.Open('./数据/1_maxfile/10y_2h.max').ReadAsArray()
# six type of landuse map
resident = np.where(landuse==1, 1, 0)
res_depth = maxdepth*resident
#
commerce = np.where(landuse==2, 1, 0)
com_depth = maxdepth*commerce

greenland = np.where(landuse==3, 1, 0)
gre_depth = maxdepth*greenland

road = np.where(landuse==4, 1, 0)
road_depth = maxdepth*road

public = np.where(landuse==5, 1, 0)
pub_depth = maxdepth*public

water = np.where(landuse==6, 0, 0)
rows, cols = landuse.shape

# damage calculation
# ---resident
# loss_res = res_depth*16.682*874.73*0.01
# loss_com = com_depth*6.8517*1372.12*0.01
# loss_roa = road_depth*4.4194*361.39*0.01
# loss_gre = gre_depth*36.304*179.14*0.01
# loss_pub = pub_depth*11.645*416.52*0.01
# setmax(loss_gre, 179.14)
# setmax(loss_roa, 361.79)



loss_res = np.clip(np.interp(res_depth,[0,0.1,0.5,1,1.5,2,3,4,5,6],[0,0,0.17,0.33,0.44,0.56,0.79,1,1,1]),0,1)
loss_com = np.clip(np.interp(com_depth,[0,0.1,0.5,1,1.5,2,3,4,5,6],[0,0,0.14,0.34,0.53,0.72,0.98,1,1,1]),0,1)
loss_roa = np.clip(np.interp(road_depth,[0,0.15,0.5,1,1.5,2,3,4,5,6],[0,0,0.36,0.57,0.73,0.85,1,1,1,1]),0,1)
loss_pub = np.clip(np.interp(pub_depth,[0,0.15,0.5,1,1.5,2,3,4,5,6],[0,0,0.25,0.42,0.55,0.65,0.8,0.9,1,1]),0,1)
loss_gre = np.clip(np.interp(gre_depth,[0,0.15,0.5,1,1.5,2,3,4,5,6],[0,0,0.26,0.47,0.62,0.91,1,1,1,1]),0,1)


loss_res = loss_res*874.73*10
loss_com = loss_com*1372.12*10
loss_roa = loss_roa*361.39*10
loss_gre = loss_gre*179.14*10
loss_pub = loss_pub*416.52*10
loss = loss_res+loss_roa+loss_com+loss_gre+loss_pub

to_raster(loss,'./结果/loss/10y_2h_2.txt')
totaldamage(loss)

# array = gdal.Open('./LID_analysis/LID_damage/Base_50y.txt').ReadAsArray()
# totaldamage(array)