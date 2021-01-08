# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import glob
import re
import datetime
from shutil import copy2
import filecmp
import time


FOLDER_TO_INSPECT = 'E:\\ElsAce3FotosFilmps'
FOLDER_TO_INSPECT = 'E:\\Noor'
FOLDER_TO_INSPECT = 'E:\\'
FOLDER_TO_INSPECT = 'E:\\els fotos 2019'
FOLDER_TO_INSPECT = 'E:\\VanComputerMoeke'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



class MyFileHandler:


    def __init__(self, inName, inTargetFolder):
        self.name = inName
        self.regexs = []
        self.targetFolder = inTargetFolder
        self.unhandledFiles = []
        self.duplicates = []
        self.handled = []

    def createNonExistingFolder(self):
        if not os.path.isdir(self.targetFolder):
            print("Going to create [%s]" % self.targetFolder)
            os.makedirs(self.targetFolder)
        else:
            print("Already existing foler [%s], not creating again" % self.targetFolder)


    def handleFile(self, inTheFile):
        matched = False
        for regex in self.regexs:
            if ( not matched ) and re.match(regex, theFile.lower()):

                matched = True
                print("the file [%s] passed the regex [%s]" % (theFile, regex))
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(inTheFile))
                print("year [%s] month [%s] day [%s]" % (mtime.year,mtime.month,mtime.day))

                ltargetFolder = os.path.join(self.targetFolder,str(mtime.year))
                ltargetFolder = os.path.join(ltargetFolder,str(mtime.month))
                ltargetFolder = os.path.join(ltargetFolder,str(mtime.day))
                print("Targetfolder [%s]" % str(ltargetFolder))

                if not os.path.isdir(ltargetFolder):
                    print("Going to create the folder [%s]" % ltargetFolder)
                    os.makedirs(ltargetFolder)

                targetFile = os.path.join(ltargetFolder, os.path.basename(theFile))

                needsCopy=True
                if os.path.isfile(targetFile):
                    if filecmp.cmp(targetFile,theFile):
                        print("Found already same destination file [%s] [%s]" % (theFile, targetFile))
                        needsCopy=False
                        self.duplicates.append(inTheFile)

                if needsCopy:
                    print("Going to copy from [%s] into [%s]" % (theFile, targetFile))
                    copy2(theFile, targetFile)
                    self.handled.append(inTheFile)

        if not matched:
            print("the file [%s] did pass any regex for the handler named [%s]" % (theFile, self.name))
            self.unhandledFiles.append(inTheFile)



def createHandlers():
    myPhotosFileHandler = MyFileHandler('photos','D:\\PhotosMoviesBackup\\Photos')
    myPhotosFileHandler.regexs.append(".*.tif")
    myPhotosFileHandler.regexs.append(".*.tiff")
    myPhotosFileHandler.regexs.append(".*.png")
    myPhotosFileHandler.regexs.append(".*.jpg")
    myPhotosFileHandler.regexs.append(".*.jpeg")
    myPhotosFileHandler.regexs.append(".*.raw")
    myPhotosFileHandler.regexs.append(".*.gif")
    myPhotosFileHandler.regexs.append(".*.bmp")

    myPhotosFileHandler2 = MyFileHandler('movies','D:\\PhotosMoviesBackup\\Movies')
    myPhotosFileHandler2.regexs.append(".*.mp4")
    myPhotosFileHandler2.regexs.append(".*.mpg")
    myPhotosFileHandler2.regexs.append(".*.avi")

    return [myPhotosFileHandler,myPhotosFileHandler2]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if not os.path.isdir(FOLDER_TO_INSPECT):
        print("Not a valid folder [%s]" % FOLDER_TO_INSPECT)
        exit(-1)

    myPhotoHandlers = createHandlers()
    for photoHandler in myPhotoHandlers:
        photoHandler.createNonExistingFolder()

    for theFile in glob.glob(FOLDER_TO_INSPECT + '\\**\\*.*'):
        print("Inspecting file [%s]" % theFile)
        for photoHandler in myPhotoHandlers:
            photoHandler.handleFile(theFile)
            #time.sleep(6)

    for photoHandler in myPhotoHandlers:
        targetFile = os.path.join(photoHandler.targetFolder,photoHandler.name+'_unhandled.txt')
        print("Saving to [%s]" % targetFile)
        with open(targetFile, "w") as outfile:
            outfile.write("\n".join(str(item) for item in photoHandler.unhandledFiles))

    for photoHandler in myPhotoHandlers:
        targetFile = os.path.join(photoHandler.targetFolder,photoHandler.name+'_duplicates.txt')
        print("Saving to [%s]" % targetFile)
        with open(targetFile, "w") as outfile:
            outfile.write("\n".join(str(item) for item in photoHandler.duplicates))

    for photoHandler in myPhotoHandlers:
        targetFile = os.path.join(photoHandler.targetFolder,photoHandler.name+'_copied.txt')
        print("Saving to [%s]" % targetFile)
        with open(targetFile, "w") as outfile:
            outfile.write("\n".join(str(item) for item in photoHandler.handled))




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
