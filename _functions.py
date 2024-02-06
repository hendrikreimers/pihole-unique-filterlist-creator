import os, sys
import requests
import tempfile
import re


# returns a list of files in a folder which matches "list-[...].txt"
# returns the fullpath including filename and just the filename
def getFilesInFolder(path: str):
    resultList = []
    for file in os.listdir(getAbsPath(path)):
        if file.endswith(".txt") and file.startswith("list-"):
            fpath = getAbsPath(os.path.join(path, file))
            resultList.append([fpath, file])

    return resultList


# creates a directory
def createDir(dirName):
    dirPath = getAbsPath(dirName)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


# returns a temp file name
def getTempFilename():
    return getAbsPath(os.path.join("tmp", next(tempfile._get_candidate_names()) + ".tmp"))


# get absolute path of this script
def getScriptPath():
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    return application_path


def getAbsPath(relPath: str):
    return os.path.abspath(getScriptPath() + ('/' + relPath).replace("/", os.sep))


def validateUri(line: str):
    urlRegex = re.compile(
        r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.]+$")  # URL validation expression
    commentRegex = re.compile(r"^#.*$")

    if not commentRegex.search(line):  # ignore something like comments
        outline = line.strip()
        if urlRegex.search(outline):
            if outline != "0.0.0.0" and outline != "127.0.0.1" and outline != "":  # dont block all ;-)
                return True

    return False


# Downloads a file by url
def download(url: str, targetFile: str):
    print("Downloading: " + url)
    print("   to: " + targetFile)

    # Some settings like the headers to be sent or whether SSL Certs should be validated and a timeout
    # I know verifying SSL is a good idea, but in some cases it isn't helpful (maybe if you're behind a proxy)
    headers     = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
    verifySsl   = True
    connTimeout = 10

    try:
        r = requests.get(url, verify=verifySsl, timeout=connTimeout, allow_redirects=True, stream=True, headers=headers)

        with open(targetFile, "wb") as targetHandle:
            if not r.ok:
                print(response)
            else:
                for chunk in r.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        targetHandle.write(chunk)
    except Exception as ex:
        print("--- Error downloading: " + url)


# concatenate files and not adding duplicates to the big file
def concatenateFiles(sourceFileList: list, targetFile: str):
    lines_seen = set()  # cache for alread read lines
    regex = r"^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}[ \t]+)?((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])([ \t]?#.*)?$"  # Domain validation expression
    commentRegex = re.compile(r"^#.*$")

    # Get the static whitelist
    with open(getAbsPath("dist/_whitelist-filter.txt")) as whitelistFile:
        staticWhitelist = [line.strip() for line in whitelistFile]  # whitelistFile.readlines()

    with open(targetFile, 'w', encoding="utf8") as outfile:  # open target file

        for fname in sourceFileList:  # run through each temp file

            if os.path.exists(fname):  # check if file really exist (maybe not due fetch errors)
                for each_line in open(fname, "r", encoding="utf8"):  # read each line in that file

                    if not commentRegex.search(each_line):  # ignore something like comments
                        matches = re.findall(regex, each_line.strip())  # find only domain names

                        if len(matches) > 0:
                            if len(matches[0]) > 0:
                                outline = matches[0][1].strip()
                                outlineToWrite = outline + '\n'  # merges to correct pihole block line

                                if outline != "0.0.0.0" and outline != "127.0.0.1" and outline != "":  # don't block them all ;-)
                                    if outline not in lines_seen:  # check if line already read

                                        # Check if the line is not in the whitelist, so it should be ignored
                                        if outline not in staticWhitelist:
                                            outfile.write(outlineToWrite)  # write to big file

                                        lines_seen.add(outline)  # cache the line so it will be not written twice

    lines_seen = []  # clear cache (maybe useless)


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
