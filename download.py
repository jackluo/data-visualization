##################### HEAD #######################

import requests
import os

from crawly import *

#################### CONFIG ######################

base_url = r"https://vincentarelbundock.github.io/Rdatasets/"
base_directory = r"Downloads/R Datasets/"

##################### MAIN #######################

response = load(base_url + "datasets.html")

csvs=[]

for line in response.text.split("\n"): 

    if 'CSV' in line: 

        start = line.index("href=")
        end = line.index(".csv")

        csvname = line[start+6:end+4]
        csvs.append(csvname)

for csvFile in csvs:

    response = load(base_url + csvname)

    filename = os.path.join(base_directory, csvFile)
    directory = os.path.dirname(filename)

    try: 
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise

    file = open(filename, "w")
    print "[Info]", "Writing to:", filename

    file.write(response.text)
    file.close()
   

