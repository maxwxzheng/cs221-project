import errno
import json
import os
import time
import urllib
import subprocess
import sys

"""
Util to sort the json files with wrong titles written by download.py
"""

#DIR_NAME = 'data_20141018-2346'
#DIR_NAME = 'data_20141019-0029'
DIR_NAME = 'data_20141019-0055'

if __name__ == '__main__':
    for filename in os.listdir(DIR_NAME):
        if filename.find('wrong') != 0:
            continue
        f = open("%s/%s" % (DIR_NAME, filename))
        print "=============="
        print f.readline().strip()
        j = json.load(f)
        print "RT title:   %s" % j['movies'][0]['title']
        sys.stdout.write('OK match? (y)> ')
        line = sys.stdin.readline().strip()
        if not line:
            continue
        if line.find('y') >= 0:
            """
            print "writing to ", filename[len('wrong-'):]
            print "deleting ", filename
            """
            out = open('%s/%s' % (DIR_NAME, filename[len('wrong-'):]), 'w')
            out.write(json.dumps(j, indent=4))
            out.close()
            os.remove('%s/%s' % (DIR_NAME, filename))
