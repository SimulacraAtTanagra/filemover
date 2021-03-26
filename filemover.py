import pathlib
import os
import datetime
import shutil
#TODO use https://stackoverflow.com/questions/1072569/see-if-two-files-have-the-same-content-in-python filecmp
def grab_dates(file):
    fname = pathlib.Path(file)
    #assert fname.exists(), f'No such file: {fname}'  # check that the file exists
    #create = datetime.datetime.fromtimestamp(fname.stat().st_ctime).year
    modify = datetime.datetime.fromtimestamp(fname.stat().st_mtime).year
    return(str(modify))
        
def foldercheck(folderstring):
    if os.path.isfile(folderstring):
        return(True)
    else:
        try:
            os.mkdir(folderstring)
            foldercheck(folderstring)
        except FileExistsError:
            return(True)
        
def try_move(filename,dest):
    filename=os.path.abspath(filename)
    dest=os.path.abspath(dest)
    try:
        shutil.move(filename,dest)
    except:
        filelist=filename.split('.')
        filenew='.'.join(filelist[:-1])+"X."+filelist[-1]
        filenew=os.path.abspath(filenew)
        try:
            os.rename(filename,filenew)
        except:
            os.rename(filename,filenew)
        try_move(filename,dest)
        
def file_mover(folderstring):
    filelist= [file for file in os.listdir(folderstring) if "." in file]
    dates=[grab_dates(os.path.join(folderstring,file)) for file in filelist]
    dates=list(set(dates))
    for date in dates:
        foldercheck(os.path.join(folderstring,date))
    for file in filelist:
        filefolder=os.path.join(folderstring,grab_dates(os.path.join(folderstring,file)))
        try_move(os.path.join(folderstring,file),filefolder)
        
def file_count(folder):
    counter=0
    for dir,subdir, files in os.walk(folder):
        for file in files:
            counter+=1
    return(counter)
    
def file_dupes(folder): #checks a directory for files with duplicate names
    filelist=[]
    for dir, subdir, files in os.walk(folder):
        for file in files:
            filelist.append(file)
    filelist=list(set(filelist))
    registration={file:[] for file in filelist}
    for dir, subdir, files in os.walk(folder):
        for file in files:
            registration[file].append(os.path.join(dir,file))
    print(len([i for i in registration.values() if len(i)>1]),"duplicates")
    return(registration)
