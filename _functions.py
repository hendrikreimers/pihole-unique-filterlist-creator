import os, sys
import wget
import tempfile
import re

# creates a directory
def createDir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)


# returns a temp file name
def getTempFilename():
    return os.path.join("tmp", next(tempfile._get_candidate_names()) + ".tmp")


# get absolute path of this script
def getScriptPath():
    pathname = os.path.dirname(__file__)
    return os.path.abspath(pathname)


# Downloads a file by url
def download(url: str, targetFile: str):
    print("Downloading: " + url)
    print("   to: " + targetFile)
	
    try:
        wget.download(url, targetFile)
    except Exception as ex:
	    print("--- Error downloading")


# concatenate files and not adding duplicates to the big file
def concatenateFiles(sourceFileList: list, targetFile: str):
    lines_seen = set() # cache for alread read lines
    regex = r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]" # Domain validation expression
    with open(targetFile, 'w') as outfile: # open target file
        for fname in sourceFileList: # run through each temp file
            if os.path.exists(fname): # check if file really exist (maybe not due fetch errors)
                for each_line in open(fname, "r"): # read each line in that file
                    if "#" not in each_line: # ignore something like comments
                        matches = re.findall(regex, each_line.strip()) # find only domain names
                        if len(matches) > 0:
                            outline = '0.0.0.0 ' + matches[0].strip() + '\n' # merges to correct pihole block line
                            if outline not in lines_seen: # check if line alread read
                                outfile.write(outline) # write to big file
                                lines_seen.add(outline) # cache the line so it will be not written twice
    
    lines_seen = [] # clear cache (maybe useless)


# deletes a list of files
def deleteFilesInList(fileList: list):
    for file in fileList:
        if os.path.exists(file):
            os.remove(file)


# print out message
def pMsg(msg: str, nl: bool = False):
    if nl == True:
	    print("")
	
    print(">>> " + msg)


