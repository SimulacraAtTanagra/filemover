# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:57:57 2021

@author: shane
"""

import pathlib
import os
import datetime
import shutil

def grab_dates(file):
    fname = pathlib.Path(file)
    assert fname.exists(), f'No such file: {fname}'  # check that the file exists
    create = datetime.datetime.fromtimestamp(fname.stat().st_ctime).year
    modify = datetime.datetime.fromtimestamp(fname.stat().st_mtime).year
    if create==modify:
        return(create)
    elif modify<create:
        return(modify)
    else:
        return(modify)
        
def foldercheck(folderstring):
    if os.path.isfile(folderstring):
        return(True)
    else:
        os.mkdir(folderstring)
        return(foldercheck(folderstring))
        
def file_mover(folderstring):
    filelist= os.listdir(folderstring)
    dates=[grab_dates(file) for file in os.listdir(folderstring)]
    dates=list(set(dates))
    for date in dates:
        foldercheck(os.path.join(folderstring,date))
    for file in filelist:
        filefolder=os.path.join(folderstring,grab_dates(os.path.join(folderstring,file)))
        shutil.move(os.path.join(folderstring,file),filefolder)
    
    