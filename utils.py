"""
calculating the exchange volumes
The Third Draft
"""
import pandas as pd
import numpy as np
import os
Co = 0.540  # 孔径系数
Cw0 = 0.418  # 堰流系数
g = 9.81  # 重力加速度

def before_step(node,wdmap,elemap,info,tstep,rowid,vmap=None):
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
            fr = vmap[x,y][0]/(g*wd)**0.5
            Cw = Cw0 * (fr ** (-0.906)) if fr > 1 else Cw0
            # Co,Cw = 0.62,0.6
            z = elemap[x,y][0]
            phi = target_row['R'].values.astype(np.int32)
            c = np.pi * phi * 0.001    # 湿周，转换成米
            a = (phi / 2 * 0.001) ** 2 * np.pi  # 管口面积转换成米
            hd = z - node.head    #检查井水面到地面距离
            # qm = a*hd/30
            if (wd - 3 * phi).all() > 0:
                surcharge = Co * a * (2 * g * wd) ** 0.5  # 计算公式不要搞错 0.62是孔口流量系数
            elif wd <= 3 * phi and (hd / (z + wd)) <= (2 / 3):
                surcharge = Cw * c * ((2 * g) ** 0.5) * ((z + wd) ** 1.5)
            else:
                surcharge = Cw * c * hd * ((2 * g * (z + wd - hd)) ** 0.5)
            node.generated_inflow(surcharge[0])
            surcharge /= 5
            with open('./prepared_bdy/' + str(tstep) + 'step.bdy', 'a') as file:
                file.writelines(node.nodeid + '\n')
                file.writelines('1   seconds\n')
                file.writelines('-' + str(surcharge[0]) + '   0' + '\n')
                file.writelines('\n')

        else:
            print(f'{node.nodeid} is taking the 4th option.')

    else:
        pass

def scan(filepath):
    filelist = os.listdir(filepath)
    print(filelist)
    for f in filelist:
        if f.split('.')[-1] in ['inittm','max','mxe','maxtm','totaltm'] or '0000' in f:
            os.remove(os.path.join(filepath, f))

def initial(name):
    with open(f'{name}.par', 'w') as f:
        f.writelines(f'#  assess rain {name} \n')
        f.writelines('\n')
        f.writelines(f'resroot   {name}_1\n')
        f.writelines(f'dirroot   {name}_res\n')
        f.writelines('bcifile   Modelpoint.bci\n')
        f.writelines('bdyfile   ./prepared_bdy/initialize.bdy\n')
        f.writelines('DEMfile    sa_2m.asc\n')
        f.writelines('#nodata_elevation   -50\n')
        f.writelines('manningfile   manninval_2.asc\n')
        f.writelines('saveint   30\n')
        f.writelines('massient   10\n')
        f.writelines('sim_time   30.0\n')
        f.writelines('initial_tstep   0.5\n')
        f.writelines('acceleration\n')
        f.writelines('#startfile        1d2dcoupled.start\n')
        f.writelines('elevoff\n')
        f.writelines('hazard\n')



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
