#! /usr/bin/env python

import os

TMP_DIR = None
if not os.environ.has_key('OPENSHIFT_TMP_DIR'):
    TMP_DIR = "./data"
else:
    TMP_DIR = os.environ['OPENSHIFT_TMP_DIR']

filelist = [ f for f in os.listdir(TMP_DIR) ]
for f in filelist:
    os.remove(os.path.join(TMP_DIR, f))
