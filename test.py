from AWSHalide import *
from imagehelp import *
import time

def query_and_run(query):
    init()
    save_images(query)
    path = "*.png"
    for fname in glob.glob(path):
        local('rm ' + PATH_TO_ZIP_DIR + '/images/image.png')
        local('mv ' + fname + ' ' + PATH_TO_ZIP_DIR + '/images/image.png')
        upload_zip(fname+'.zip')






