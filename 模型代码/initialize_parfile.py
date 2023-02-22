def initial(filename):
    with open(filename, 'w') as f:
        f.writelines('#  assess single LID-GR at small size 50y \n')
        f.writelines('\n')
        f.writelines('resroot   LID_BC_1\n')
        f.writelines('dirroot   LID_BC_res2\n')
        f.writelines('bcifile   Modelpoint.bci\n')
        f.writelines('bdyfile   ./prepared_bdy/initialize.bdy\n')
        f.writelines('DEMfile    sa_2m.asc\n')
        f.writelines('#nodata_elevation   -50\n')
        f.writelines('manningfile   manninval_2.asc\n')
        f.writelines('saveint   30\n')
        f.writelines('massient   10\n')
        f.writelines('sim_time   30.0\n')
        f.writelines('initial_tstep   0.1\n')
        f.writelines('acceleration\n')
        f.writelines('#startfile        1d2dcoupled.start\n')
        f.writelines('elevoff\n')













