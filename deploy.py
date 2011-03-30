from simples3 import *
from pprint import pprint
import os, sys
import re

# Config options
ACCESS_KEY='AKIAJIKKXWQITYQM6RFA'
SECRET_KEY='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'
BUCKET_NAME = "umbrant"
BASE_URL='https://s3-us-west-1.amazonaws.com/umbrant'

SOURCE_DIR="/home/andrew/umbrant/www/umbrant"

IGNORE = (
          "\.(.*).swp$", "~$", # ignore .swp files
         )

# code

ignore_re = []
for i in IGNORE:
    ignore_re.append(re.compile(i))

# open bucket
bucket = S3Bucket(BUCKET_NAME, access_key=ACCESS_KEY, secret_key=SECRET_KEY, base_url=BASE_URL)

# recursively put in all files in SOURCE_DIR

for root, dirs, files in os.walk(SOURCE_DIR):
    relroot = root[len(SOURCE_DIR)+1:]
    for f in files:
        # root directory files should not have a preceding "/"
        # puts the files in a blank named directory, not what we want
        key = ""
        if relroot:
            key = relroot + "/" + f
        else:
            key = f
        filename = root + "/" + f

        # check in the ignore list
        ignore = False
        for i in ignore_re:
            if re.match(i, f):
                print "Ignoring", key
                ignore = True
        if ignore:
            continue

        # check if it's changed with modtimes
        sf = False
        try:
            sf = bucket.info(key)
        except:
            contents = open(filename).read()
            bucket.put(key, contents, acl="public-read", metadata=metadata)
            print "Uploading", key
            continue

        stat = os.stat(filename)
        metadata = {"modtime":str(stat.st_mtime)}

        if not sf["metadata"].has_key("modtime") or sf["metadata"]["modtime"] != str(stat.st_mtime):
            bucket.put(key, open(filename).read(), acl="public-read", metadata=metadata)
            print "Uploading", key
            continue

        print "Skipping", key
