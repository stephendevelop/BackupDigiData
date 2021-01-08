import os
import glob
import re
import datetime

FOLDER_TO_INSPECT = 'E:\\PhotosMoviesBackup\\Photos\\2017\\1'


FOTOS_TARGET_FOLDER = 'E:\\PhotosMoviesBackup\\Photos'
MOVIES_TARGET_FOLDER = 'D:\\PhotosMoviesBackupTEST\\Movies'

PHOTO_REGEXS  = [".*.tif", ".*.tiff", ".*.png", ".*.jpg", ".*.jpeg", ".*.raw", ".*.gif", ".*.bmp"]
MOVIES_REGEXS = [".*.mp4", ".*.mpg", ".*.avi"]

def createFolder( inMtime, inPath, inFile ):
    thePath = os.path.join(inPath,str(inMtime.year))
    thePath = os.path.join(thePath,str(inMtime.month))
    thePath = os.path.join(thePath,str(inMtime.day))
    thePath = os.path.join(thePath,os.path.basename(inFile))
    return thePath

def filterOut(inFile, inRegexs):
    return any( [re.match(theRegex, inFile) for theRegex in inRegexs ] )

def handleFlavor( inRegExs, inPath ):

    thePhotoFiles = [theFile for theFile in glob.glob(FOLDER_TO_INSPECT + '\**\*.*', recursive=True) if filterOut(theFile,inRegExs)]
    thePhotoFilesWithMtime = [ (theFile, datetime.datetime.fromtimestamp(os.path.getmtime(theFile))) for theFile in thePhotoFiles ]
    thePhotoFilesWithFolders  = map( lambda theFileTuple : (theFileTuple[0], createFolder(theFileTuple[1],inPath,theFileTuple[0])), thePhotoFilesWithMtime)


    return thePhotoFilesWithFolders

if __name__ == '__main__':

    if not os.path.isdir(FOLDER_TO_INSPECT):
        print("Not a valid folder [%s]" % FOLDER_TO_INSPECT)
        exit(-1)

    print(list(handleFlavor(PHOTO_REGEXS,FOTOS_TARGET_FOLDER))[0:3])

