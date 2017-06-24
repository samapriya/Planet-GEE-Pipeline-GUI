import os
import csv
import getpass
def upload(user,source_path,destination_path,metadata_path,nodata_value):
    os.system("python ppipe.py upload -u "+str(user)+" --source "+str(source_path)+" --dest "+str(destination_path)+" -m "+str(metadata_path)+" --nodata "+str(nodata_value))
