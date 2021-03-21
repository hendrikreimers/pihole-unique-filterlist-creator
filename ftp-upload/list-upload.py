# Alternate include path
import sys, os
sys.path.append("../".replace("/", os.sep))

import ftp_user as user
from ftplib import FTP,FTP_TLS
import _functions as f

# Secure or not secure
if user.FTP_TLS:
    ftpConn = FTP_TLS()
else:
    ftpConn = FTP()

# Start FTP connection
ftpConn.connect(user.FTP_HOST, user.FTP_PORT)
ftpConn.login(user.FTP_USER, user.FTP_PASS)

# Change target folder
ftpConn.cwd(user.FTP_TARGET_DIR)

# Get local file list
localFileList = f.getFilesInFolder(user.FTP_SOURCE_DIR.replace("/", os.sep))

# Upload file list
if len(localFileList) > 0:
    for localFile in localFileList:
        fp = open(localFile[0], 'rb')
        ftpConn.storbinary('STOR ' + localFile[1], fp)
        fp.close()

# close connection
ftpConn.close()

print("")
print("FINISHED")
