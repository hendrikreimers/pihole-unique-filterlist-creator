import argparse
import importlib
import os, re

parser = argparse.ArgumentParser(description="Select mode for list generation (default is ABP Style).")
parser.add_argument('--mode', type=str, choices=['default', 'old'], default='default', help='Mode to select functions module (_functions or _functions-old).')

args = parser.parse_args()

if args.mode == 'old':
    functions_module = importlib.import_module('_functions-old')
else:
    functions_module = importlib.import_module('_functions')

f = functions_module

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

            if f.validateUri(downloadUrl):
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
