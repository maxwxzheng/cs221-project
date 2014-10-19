import errno
import json
import os
import time
import urllib
import subprocess
import sys
import re

"""
Traverses the search results and outputs a single TSV file
"""

IN_DIR_NAME = 'data'
OUT_FILE_NAME = 'rotten_tomatoes.tsv'


def process_file(filename):
    print "processing %s" % filename
    f = open("%s/%s" % (IN_DIR_NAME, filename))
    movie_id = filename[:-len(".json")]
    j = json.load(f)
    movie = j['movies'][0]
    ratings = movie['ratings']
    return '\t'.join([movie_id,
            movie['id'],
            str(ratings.get('critics_score', 0)),
            str(ratings.get('critics_rating', 0)),
            str(ratings.get('audience_score', 0)),
            str(ratings.get('audience_rating', 0)),
            ])

if __name__ == '__main__':
    # Unbuffered tee
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    tee = subprocess.Popen(["tee", "export-log.txt"], stdin=subprocess.PIPE)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())

    f = open(OUT_FILE_NAME, 'w')
    print "Writing to %s" % OUT_FILE_NAME

    # process files
    f.write('\t'.join(['imdb_movie_id',
             'rt_movie_id',
             'critics_score',
             'critics_rating',
             'audience_score',
             'audience_rating',
            ]))
    f.write('\n')
    cnt = 0
    for filename in os.listdir(IN_DIR_NAME):
        if (filename.find('wrong') != 0 and
            filename.find('swp') < 0 and
            filename.find('processed') != 0 and
            filename.find('.json') > 0):
            row = process_file(filename)
            f.write(row + '\n')
    f.close()
