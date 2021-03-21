import _functions as f
import os, re

# create some folder
f.createDir("tmp")
f.createDir("dist")

# Build a list of URL files
urlFileLists = f.getFilesInFolder("urlLists")

# Run through file list and create the url list and get the content
commentRegex = re.compile(r"^#.*$")
for urlFile in urlFileLists:
    urlList     = open(urlFile[0], 'r', encoding = 'utf8').readlines()
    tmpFileList = []
    distFile    = f.getAbsPath(os.path.join("dist", urlFile[1]))
    
    f.deleteFilesInList([distFile])
    
    for url in urlList:
        if not commentRegex.search(url): # ignore something like comments
            tmpFileName = f.getTempFilename()
            downloadUrl = url.strip()

            f.pMsg("Downloading...", True)
            f.download(downloadUrl, tmpFileName)
            tmpFileList.append(tmpFileName)
            f.pMsg("Done")

    f.pMsg("Building list in: " + distFile, True)
    f.concatenateFiles(tmpFileList, distFile)
    f.pMsg("Done.")

    f.pMsg("Cleaning temp files...", True)
    f.deleteFilesInList(tmpFileList)
    f.pMsg("Done.")

# all done
f.pMsg("FINISHED", True)
print("")
