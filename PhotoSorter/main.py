# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import glob
import re
from shutil import copy2
import filecmp
import json
import time
from itertools import product
from datetime import datetime
from PIL import Image
from datetime import date

FOLDER_TO_INSPECT = 'E:\\ElsAce3FotosFilmps'
FOLDER_TO_INSPECT = 'E:\\Noor'
FOLDER_TO_INSPECT = 'E:\\'

FOLDER_TO_INSPECT = 'E:\\VanComputerMoeke'
FOLDER_TO_INSPECT = 'E:\\PhotosMoviesBackup\\Photos\\2017\\1'
FOLDER_TO_INSPECT = 'E:\\PhotosMoviesBackup\\Photos\\2017\\1'
FOLDER_TO_INSPECT = 'D:\\GoogleBackup\working\\takeout-20210712T205043Z-001\\Takeout\\Google Foto_s\\Kids'
FOLDER_TO_INSPECT = 'D:\\GoogleBackup\working\Camera'

FOLDER_TO_INSPECT = 'D:\\GoogleBackup\\28122021\\Kids'
FOLDER_TO_INSPECT = 'F:\\'
FOLDER_TO_INSPECT = 'F:\\els fotos 2019'
FOLDER_TO_INSPECT = 'D:\\PhotosMoviesBackup\\Photos'




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def getmtime(theFile):
        theJsonFromGoogle = "%s.json" % str(theFile)
        if os.path.isfile(theJsonFromGoogle):
            print("Found googlejson ... gonna parse")
            with open(theJsonFromGoogle) as fileFromJson:
                jsonfromgoogle = json.load(fileFromJson)
                print(jsonfromgoogle['creationTime']['timestamp'])
                theTimeFromJsonGoogle = datetime.fromtimestamp( int(jsonfromgoogle['creationTime']['timestamp'] ))
                print(theTimeFromJsonGoogle)
                return theTimeFromJsonGoogle
        else:
            print("Did not find googlejson ... gonna use timestamp of file")            
            return datetime.fromtimestamp(os.path.getmtime(theFile))

def getImageDateTimeOutOfExif(fn):
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    exif = Image.open(fn)._getexif()
 
    for t in tags:
        dat = exif.get(t[0])
        sub = exif.get(t[1], 0)
 
        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat = dat[0] if type(dat) == tuple else dat
        sub = sub[0] if type(sub) == tuple else sub
        if dat != None: break
 
    if dat == None: return None
    full = '{}.{}'.format(dat, sub)
    T = datetime.strptime(full, std_fmt)
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return T

class MyFileHandler:


    def __init__(self, inName, inTargetFolder):
        self.name = inName
        self.regexs = []
        self.targetFolder = inTargetFolder
        self.unhandledFiles = []
        self.duplicates = []
        self.handled = []
        self.offtime = []
        self.warnings = []

    def createNonExistingFolder(self):
        if not os.path.isdir(self.targetFolder):
            print("Going to create [%s]" % self.targetFolder)
            os.makedirs(self.targetFolder)
        else:
            print("Already existing foler [%s], not creating again" % self.targetFolder)


   

    def handleFile(self, theFile):
        print(" ++++++++++++++++ handling file [%s] +++++++++++++++++++++" % str(theFile))
        
        matched = False
        msg = None
        for regex in self.regexs:            
            if ( not matched ) and re.match(regex, theFile.lower()):

                matched = True
                print("the file [%s] passed the regex [%s]" % (theFile, regex))
                workDateTime = None


                ######################################
                # GetFileNameDate
                ######################################
                match = re.search("(20[0-2][0-9][0-1][0-9][0-2][0-9])", theFile)
                filenameDate = None
                if match is not None:
                    filenameDate = datetime.strptime(match.group(), '%Y%m%d')
                    print("Filenamedate [%s] " % str(filenameDate))

                ######################################
                #Get Mtime from file
                ######################################
                mtime = getmtime(theFile)

                ######################################
                #GetExifDateTime
                ######################################
                exifDateTime = None
                try:
                    exifDateTime = getImageDateTimeOutOfExif(theFile)
                except Exception as e:
                    print("error during exif [%s]" % str(e))


                

                '''
                if exifDateTime is not None:
                    print("mtime [%s] exifdatetime [%s]" % ( str(mtime), str(exifDateTime) ))
                    timeDelta = (int((exifDateTime - mtime).total_seconds() / 3600))*-1
                    print("TimeDelta [%s]" % str(timeDelta))
                    if timeDelta >24:
                        msg =  "%s -> !!! exifDateTime differs => exifdatetime[%s]  mtime[%s]" % (str(theFile),str(exifDateTime),str(mtime))   
                        self.offtime.append(msg)                     
                        print(msg)
                        continue
                '''

                if filenameDate is not None:   
                    if (exifDateTime is None):
                        workDateTime = filenameDate
                    elif (exifDateTime is not None) and ((int((filenameDate - exifDateTime).total_seconds() / 3600 ))*-1) <= 25:
                        workDateTime = exifDateTime
                    else:
                        msg =  "%s -> !!! filenamedate found, but exifdate too much off !!! exifdatetime[%s]  mtime[%s] filenamedate[%s]" % (str(theFile),str(exifDateTime),str(mtime),str(filenameDate))   
                        self.offtime.append(msg)  
                        continue                                                                    
                else:
                    if (mtime is not None) and (exifDateTime is not None):
                        timeDeltaHours = (int((exifDateTime - mtime).total_seconds() / 3600))*-1 
                        if timeDeltaHours > 48:
                            msg =  "%s -> !!! using exifdatetime, exifDateTime vs mtime differs very much => exifdatetime[%s]  mtime[%s] filenamedate[%s]" % (str(theFile),str(exifDateTime),str(mtime),str(filenameDate))   
                            self.warnings.append(msg)                             
                        #Exif always has priority over mtime, because mtime is time when saved
                        workDateTime = exifDateTime
                    elif mtime is None and exifDateTime is None:
                        msg =  "%s -> !!! no date found !!! exifdatetime[%s]  mtime[%s] filenamedate[%s]" % (str(theFile),str(exifDateTime),str(mtime),str(filenameDate))   
                        self.offtime.append(msg)  
                        continue   
                    elif mtime is None:
                        workDateTime = exifDateTime
                    elif exifDateTime is None:
                        workDateTime = mtime
                    else:
                        raise Exception("Should never get here!!!!!!!!!!!!!!!!!!!")
                                    


                mtime = workDateTime

                print("Gonna handle file with year [%s] month [%s] day [%s]" % (mtime.year,mtime.month,mtime.day))

                ltargetFolder = os.path.join(self.targetFolder,str(mtime.year))
                ltargetFolder = os.path.join(ltargetFolder,str(mtime.month))
                ltargetFolder = os.path.join(ltargetFolder,str(mtime.day))
                print("Targetfolder [%s]" % str(ltargetFolder))

                if not os.path.isdir(ltargetFolder):
                    print("Going to create the folder [%s]" % ltargetFolder)
                    os.makedirs(ltargetFolder)

                targetFile = os.path.join(ltargetFolder, os.path.basename(theFile))
                
                if os.path.isfile(targetFile):
                    if filecmp.cmp(targetFile,theFile):
                        print("Found already same destination file [%s] [%s]" % (theFile, targetFile))
                        self.duplicates.append(theFile)                
                    else:
                        self.unhandledFiles.append("CAUTION:::::: Same filename, different content, no copy taken => sourcefile[%s] targetfile [%s]" % (str(theFile),str(targetFile) ))                        
                else:
                    print("Going to copy from [%s] into [%s]" % (theFile, targetFile))
                    copy2(theFile, targetFile)
                    self.handled.append("copied [%s] into [%s] with msg [%s]" % (theFile,targetFile,str(msg)))

        if not matched:
            print("the file [%s] did not pass any regex for the handler named [%s]" % (theFile, self.name))
            self.unhandledFiles.append(theFile)
        #time.sleep(2)



def createHandlers():
    myPhotosFileHandler = MyFileHandler('photos','C:\\TEMPFotos')
    myPhotosFileHandler.regexs.append(".*.tif$")
    myPhotosFileHandler.regexs.append(".*.tiff$")
    myPhotosFileHandler.regexs.append(".*.png$")
    myPhotosFileHandler.regexs.append(".*.jpg$")
    myPhotosFileHandler.regexs.append(".*.jpeg$")
    myPhotosFileHandler.regexs.append(".*.raw$")
    myPhotosFileHandler.regexs.append(".*.gif$")
    myPhotosFileHandler.regexs.append(".*.bmp$")

    myPhotosFileHandler2 = MyFileHandler('movies','C:\\TEMPMovies')
    myPhotosFileHandler2.regexs.append(".*.mp4$")
    myPhotosFileHandler2.regexs.append(".*.mpg$")
    myPhotosFileHandler2.regexs.append(".*.avi$")

    return [myPhotosFileHandler,myPhotosFileHandler2]


def writeListOut(inTargetFile, inList):
    print("Saving List to [%s]" % inTargetFile)
    with open(inTargetFile, "w") as outputFile:
        outputFile.write("\n".join(str(item) for item in inList))



def writeOutResults(photoHandler):

    today = date.today()
    d1 = today.strftime("%d_%m_%Y")
    createTargetFileName = lambda photoHanlder, suff: os.path.join(photoHandler.targetFolder, photoHandler.name + suff)

    targetFile = createTargetFileName(photoHandler, '%s_unhandled.txt' % str(d1))
    print("Saving unhandled to [%s]" % targetFile)
    writeListOut(targetFile, photoHandler.unhandledFiles)

    targetFile = createTargetFileName(photoHandler, '%s_duplicates.txt' % str(d1) )
    print("Saving duplicates to [%s]" % targetFile)
    writeListOut(targetFile, photoHandler.duplicates)

    targetFile = createTargetFileName(photoHandler, '%s_copied.txt' % str(d1))
    print("Saving copied to [%s]" % targetFile)
    writeListOut(targetFile, photoHandler.handled)

    targetFile = createTargetFileName(photoHandler, '%s_warnings.txt' % str(d1))
    print("Saving warnings to [%s]" % targetFile)
    writeListOut(targetFile, photoHandler.warnings)

    targetFile = createTargetFileName(photoHandler, '%s_offtime.txt' % str(d1))
    print("Saving offtime to [%s]" % targetFile)
    writeListOut(targetFile, photoHandler.offtime)

    return "x"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if not os.path.isdir(FOLDER_TO_INSPECT):
        print("Not a valid folder [%s]" % FOLDER_TO_INSPECT)
        exit(-1)

    myPhotoFileHandlers = createHandlers()
    for photoFileHandler in myPhotoFileHandlers:
        photoFileHandler.createNonExistingFolder()

    [photoHandler.handleFile(theFile) for photoHandler in myPhotoFileHandlers for theFile in  glob.glob(FOLDER_TO_INSPECT + '\\**\\*.*', recursive=True)]
    list(map(writeOutResults, myPhotoFileHandlers))

