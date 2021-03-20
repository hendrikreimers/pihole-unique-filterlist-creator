import _functions as f
import os

# create some folder
f.createDir("tmp")
f.createDir("build")

# get some basics
urlListFile = open('urlList.txt', 'r')
urlList     = urlListFile.readlines()
tmpFileList = []
#buildFile   = f.getAbsPath("build/blacklist.txt")
buildFile   = "build/blacklist.txt".replace("/", os.sep)

i = 0

# delete old list
f.deleteFilesInList([buildFile])

# get downloads
for url in urlList:
    tmpFileName = f.getTempFilename()
    downloadUrl = url.strip()
    
    f.pMsg("Downloading...", True)
    f.download(downloadUrl, tmpFileName)
    tmpFileList.append(tmpFileName)
    f.pMsg("Done")

# build big list
bigListTmpFile = f.getTempFilename()
f.pMsg("Building list in: " + buildFile, True)
f.concatenateFiles(tmpFileList, buildFile)
f.pMsg("Done.")

# clear temp
f.pMsg("Cleaning temp files...", True)
f.deleteFilesInList(tmpFileList)
f.pMsg("Done.")

# all done
f.pMsg("FINISHED", True)
print("")
