import os
import shutil
from pyswmm import Simulation, Nodes
import pandas as pd
from osgeo import gdal
import numpy as np
import initialize_parfile as inip
import cal_flow as cf
import del_2dtempfile as d2t   #删除临时文件模块

# 运行第一个时间步长的2d-model和swmm模型
sim = Simulation('./LID_BC_30y/CModel_BC2.inp')
sim.step_advance(30)
sim.start()
sim.next()
os.chdir('./LID_BC_30y')
inip.initial('./LID_BC.par')   # 重写parfile，模型从头开始运行
os.system('..\lisflood.exe -log LID_BC.par')  # 第一次运行
print('lisflood is running the first time..')


# 开始一个步长一个步长的循环计算
t = 1
manhole_chart = pd.read_csv('../Interacfile.txt')  #interaction file:写有检查井ID、xy坐标、地表高程、检查井面积、所在栅格序号信息
elemap = gdal.Open('./sa_2m.asc').ReadAsArray()
rowncolumns = gdal.Open('../rowncol.asc').ReadAsArray()   #rowncol file:给每个栅格标有序号的ASC文件

for step in range(1, 240):
    # 准备.bdy文件的第一行
    with open('./prepared_bdy/'+str(t)+'step.bdy','a') as f:
        f.writelines('comment line\n')
    #准备waterdepth文件
    print("t="+str(t))
    wdpath= './LID_BC_res2/LID_BC_'+str(t)+'-0001.wd'
    print(wdpath)
    print(os.getcwd())
    wdmap = gdal.Open(wdpath).ReadAsArray()
    # print(type(wdmap))
    # 初始化节点
    nodes = Nodes(sim)
    for node in nodes:
        cf.before_step(node,wdmap,elemap,manhole_chart,t,rowncolumns)
    print('the current time is：'+f'{sim.current_time}')
    sim.next()

    # 复制结果的wd文件到上一级文件夹，并重新命名为.start文件
    temp = './1d2dcoupled.start'
    shutil.copy(wdpath, temp)
    print('startfile was ready.')

    # 对par文件进行修改，并且开始下一时间步长的lisflood-fp模拟
    # 三个部分的par文件需要改写：结果文件名字根据次数变动，每一分钟的bdy文件不一样，startfile也不一样
    t = t + 1
    rf = open('./LID_BC.par', 'r+')
    fcontent = rf.readlines()
    fcontent[2] = 'resroot         LID_BC_'+str(t)+'\n'
    print(fcontent[2])
    fcontent[5] = 'bdyfile           ./prepared_bdy/'+str(t-1)+'step.bdy'+'\n'
    print(fcontent[5])
    fcontent[14] = 'startfile        1d2dcoupled.start'+'\n'
    print(fcontent[14])
    rf.close()
    rf = open('./LID_BC.par', 'w+')
    rf.writelines(fcontent)
    rf.close()
    print('parfile was ready.')
    os.system(r'..\lisflood.exe -log  LID_BC.par')

    # delete unnecessary result file
    d2t.scan('./LID_BC_res2')
    os.chdir(r'D:\实验\5_08_the_new_coupling\LID_BC_30y')

# sim.report()
sim.close()