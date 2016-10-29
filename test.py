##################### TIME #######################

import time
start_time = time.time()

##################### HEAD #######################

import collections
import os
import csv

import requests
from requests.auth import HTTPBasicAuth

#################### CONFIG ######################

base_directory = r"Downloads"
auth = HTTPBasicAuth('datasets', 'w581yrzokp')
headers = {'Plotly-Client-Platform': 'python'}

################## FUNCTIONS #####################


# gets a list of filenames recursively from base directory
def get_filenames(base_directory):

    list_of_filenames = []

    for root, directories, filenames in os.walk(base_directory):

        for filename in filenames:

            filename = os.path.join(root,filename)
            if not filename.endswith(".DS_Store") : list_of_filenames.append(filename)

    return list_of_filenames


# column name is header of the csv. corresponding to the first row of the csv
def extract_column_data(filename, column_names):

    columns = []

    for column_name in column_names:
        # opens csv as a dictreader object and assigns it to variable reader
        column = []

        reader = csv.DictReader(open(filename, 'rU'))
        for row in reader:
            column.append(row[column_name].strip())

        columns.append(column)
    
    return columns


# beautifies the filename for upload
def get_title(filename):

    if filename.endswith(".csv"):
        filename = filename[:-4]
    
    if filename.startswith("Downloads"):
        filename = filename[9:]

    filename = filename.replace("_", " ").replace("-", " ").replace(".", " ")
    return filename.title()


# makes the folder payload to create a folder
def make_folder(directory):

    nested_dict = lambda: collections.defaultdict(nested_dict)
    folder_payload = nested_dict()

    folder_payload["path"] = get_title(directory)
    return folder_payload


# makes the Plotly Grid object with the columns and the title
def make_payload(columns, column_names, filename, folder_payload):

    # check for duplicates in list as Plotly doesnt support columns with same name
    dups = {}

    for i, val in enumerate(column_names):
        if val not in dups:
            # Store index of first occurrence and occurrence value
            dups[val] = [i, 1]
        else:
            # Special case for first occurrence
            if dups[val][1] == 1:
                column_names[dups[val][0]] += str(dups[val][1])

            # Increment occurrence value, index value doesn't matter anymore
            dups[val][1] += 1

            # Use stored occurrence value
            column_names[i] += str(dups[val][1])

    # creates nested dictionnary
    nested_dict = lambda: collections.defaultdict(nested_dict)
    payload = nested_dict()

    payload["filename"] = get_title(filename)
    payload["title"] = get_title(filename)
    payload["world_readable"] = True
    payload["parent_path"] = folder_payload["path"]
 
    for i, column in enumerate(columns):
        payload["data"]["cols"][column_names[i]]["order"] = i
        payload["data"]["cols"][column_names[i]]["data"] = column

    return payload


##################### MAIN #######################


filenames = get_filenames(base_directory)
old_folder_payloads = [None, ]

for filename in filenames:

    # open the csv first to get the column_names to use csv as dictreader
    file = open(filename, 'rU')

    # opens once to get the column names
    column_names = csv.reader(file).next()
    column_names = [column_name.strip() for column_name in column_names]
    columns = extract_column_data(filename, column_names)    
    
    root, rootless_filename = os.path.split(filename)
    folder_payload = make_folder(root)
    payload = make_payload(columns, column_names, rootless_filename, folder_payload)

    print payload["filename"]
    print folder_payload["path"],  payload["parent_path"]

    if folder_payload != old_folder_payloads[-1]:
        folder_response = requests.post('https://api.plot.ly/v2/folders', auth=auth, headers=headers, json=folder_payload)
        print "Created folder"
        print "FOLDER", folder_response.text

    else:
        print "Skipped"

    response = requests.post('https://api.plot.ly/v2/grids', auth=auth, headers=headers, json=payload)
    print "GRID", response.text
    
    old_folder_payloads.append(folder_payload) 

##################### TIME #######################

print "Done!"
print "%s seconds" % (time.time() - start_time)


 


 
