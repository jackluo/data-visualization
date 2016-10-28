##################### TIME #######################

import time
start_time = time.time()

##################### HEAD #######################

import os
import csv
import requests

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Column, Grid

#################### CONFIG ######################

base_directory = r"Downloads"
# ADD PRIVATE API KEY HERE TO CHANGE ACCOUNT

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


def get_title(filename):

    if filename.endswith(".csv"):
        filename = filename[:-4]
    
    filename = filename.replace("Downloads/", "").replace("_", " ").replace("-", " ").replace(".", " ")
    return filename.title()


# makes the Plotly Grid object with the columns and the title
def make_grid(columns, column_names, filename):

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


    # list comprehension to create a list of Column objects used to make Grid
    # get_title gets the capitalized title for csv file    
    column_data = [Column(column, column_names[i]) for i, column in enumerate(columns)]
    grid = Grid(column_data)
    title = get_title(filename)

    return grid, title


##################### MAIN #######################


list_of_filenames = get_filenames(base_directory)

for filename in list_of_filenames:

    # open the csv first to get the column_names to use csv as dictreader
    file = open(filename, 'rU')

    column_names = csv.reader(file).next()
    column_names = [column_name.strip() for column_name in column_names]

    columns = extract_column_data(filename, column_names)    
    
    grid, title = make_grid(columns, column_names, filename)
    print title

    #grid_url = requests.get('https://api.plot.ly/v2/files/lookup', params={'user': 'datasets', 'path': title}).json()["web_url"]
    #print grid_url
    #py.grid_ops.delete(grid_url=grid_url)

    grid_url = py.grid_ops.upload(grid, filename=title, world_readable=True, auto_open=True)


##################### TIME #######################

print "Done!"
print "%s seconds" % (time.time() - start_time)
