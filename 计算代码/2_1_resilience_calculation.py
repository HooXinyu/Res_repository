from osgeo import gdal
import numpy as np
import pandas as pd
import os
import Tools_SetNull as tools

# def to_raster(array,filepath):
#     df = pd.DataFrame(array)
#     with open(filepath, 'w+') as f:
#         f.writelines('ncols         694\n')
#         f.writelines('nrows         824\n')
#         f.writelines('xllcorner     581104.93980083\n')
#         f.writelines('yllcorner     3495917.0924138\n')
#         f.writelines('cellsize      2\n')
#         f.writelines('NODATA_value  -9999\n')
#         f.close()
#     df.to_csv(filepath, sep=' ', columns=None, index=False, header=False, mode='a+',float_format='%.3f')


landuse = gdal.Open('./landuse.txt').ReadAsArray()


resident = np.where(landuse==1, 1, 0)
commerce = np.where(landuse==2, 1, 0)
greenland = np.where(landuse==3, 1, 0)
road = np.where(landuse==4, 1, 0)
public = np.where(landuse==5, 1, 0)
water = np.where(landuse==6, 1, 0)


filelist = os.listdir('./LID_VS_50y/LID_VS_res')
print(filelist)

box = []
for f in filelist:
    if f[-3:] == '.wd':
        wd = gdal.Open('./LID_VS_50y/LID_VS_res/'+f).ReadAsArray()

        resident_depth = wd*resident
        com_depth = wd*commerce
        gre_depth = wd*greenland
        road_depth = wd*road
        pub_depth = wd*public
        water_depth = wd*water


        green_res = greenland - gre_depth/2
        water_res =water - water_depth/2
        green_res[green_res < 0] = 0
        water_res[water_res < 0] = 0


        resident_res = resident - resident_depth/0.3
        com_res = commerce - com_depth/0.3
        road_res = road - road_depth/0.3
        pub_res = public - pub_depth/0.3
        resident_res[resident_res < 0] = 0
        com_res[com_res < 0] = 0
        road_res[road_res < 0] = 0
        pub_res[pub_res < 0] = 0


        x = (green_res+water_res+resident_res+com_res+road_res+pub_res)*0.5
        box.append(x)
total = sum(box)
res = total/120

tools.setnull(res,landuse)
tools.to_asc(res, './LID_analysis/LID_resilience/LID_VS3_50y.txt')
