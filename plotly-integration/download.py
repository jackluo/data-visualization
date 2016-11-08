##################### TIME #######################

import time
start_time = time.time()

##################### HEAD #######################

import requests
import os

#################### CONFIG ######################

base_url = r"https://vincentarelbundock.github.io/Rdatasets/"
base_directory = r"Downloads/R Datasets/"

################### FUNCTIONS ####################


def load(url, params = None, headers = {}):

    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    if headers == -1:
        headers = None
    
    response = requests.get(url, params = params, headers = headers)
    return response


##################### MAIN #######################


response = load(base_url + "datasets.html")

csvs=[]

for line in response.text.split("\n"): 

    if 'CSV' in line: 

        start = line.index("href=")
        end = line.index(".csv")

        csvname = line[start+6:end+4]
        csvs.append(csvname)

for csvname in csvs:

    response = load(base_url + csvname)

    filename = os.path.join(base_directory, csvname)
    directory = os.path.dirname(filename)

    try: 
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise

    file = open(filename, "w")
    print "[Info]", "Writing to:", filename

    file.write(response.text.encode('utf-8'))
    file.close()
   

##################### TIME #######################

print "Done!"
print "%s seconds" % (time.time() - start_time)