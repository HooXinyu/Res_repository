"""
calculating the exchange volumes
The Third Draft
"""
from pyswmm import Simulation, Nodes
import pandas as pd
from osgeo import gdal
import numpy as np


def before_step(node,wdmap,elemap,info,tstep,rowid):
    target_row = info[info['NODEID']==node.nodeid]
    # print(node.nodeid)
    # print(target_row)
    rasterid = target_row['gridcode'].values
    if rasterid[0] > 0:
        x, y = np.where(rowid==rasterid)
        wd = wdmap[x,y][0]
        if node.flooding == 0 and wd.all() <= 1e-4:
            node.generated_inflow(0)
            print(f'{node.nodeid} is taking the 1st option')
            with open('./prepared_bdy/' + str(tstep) + 'step.bdy', 'a') as file:
                file.writelines(node.nodeid + '\n')
                file.writelines('1   seconds\n')
                file.writelines(str(node.flooding/1000/5) + '   0\n')
                file.writelines('\n')

        elif node.flooding != 0:
            node.generated_inflow(0)
            print(f'{node.nodeid} is taking the 2nd option')
            with open('./prepared_bdy/' + str(tstep) + 'step.bdy', 'a') as file:
                file.writelines(node.nodeid + '\n')
                file.writelines('1   seconds\n')
                file.writelines(str(node.flooding/1000/5) + '   0\n')
                file.writelines('\n')

        elif node.flooding == 0 and wd.any() > 1e-4:
            # calculate exchange volume
            print(f'{node.nodeid} is taking the 3rd option')
            z = elemap[x,y][0]
            phi = target_row['R'].values.astype(np.int32)
            c = np.pi * phi * 0.001    # 湿周，转换成米
            a = (phi / 2 * 0.001) ** 2 * np.pi  # 管口面积转换成米
            hd = z - node.head    #检查井水面到地面距离
            # qm = a*hd/30
            if (wd - 3 * phi).all() > 0:
                surcharge = 0.62 * a * (2 * 9.8 * wd) ** 0.5  # 计算公式不要搞错 0.62是孔口流量系数
            elif wd <= 3 * phi and (hd / (z + wd)) <= (2 / 3):
                surcharge = 0.6 * c * ((2 * 9.8) ** 0.5) * ((z + wd) ** 1.5)
            else:
                surcharge = 0.6 * c * hd * ((2 * 9.8 * (z + wd - hd)) ** 0.5)
            node.generated_inflow(surcharge[0])
            sur = surcharge/5
            with open('./prepared_bdy/' + str(tstep) + 'step.bdy', 'a') as file:
                file.writelines(node.nodeid + '\n')
                file.writelines('1   seconds\n')
                file.writelines('-' + str(sur[0]) + '   0' + '\n')
                file.writelines('\n')

        else:
            print(f'{node.nodeid} is taking the 4th option.')

    else:
        pass









