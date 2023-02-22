'''
remove the unnecessary file from result directory
'''
import os

def scan(filepath):
    filelist = os.listdir(filepath)
    print(filelist)
    os.chdir(filepath)
    for f in filelist:
        if f[-7:] == '.inittm' or f[-4:]=='.max' or f[-4:]=='.mxe' or f[-6:]=='.maxtm' or f[-8:]=='.totaltm' or f[-7:]=='0000.wd':
            os.remove(f)


