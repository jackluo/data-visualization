##################### TIME #######################

import time
start_time = time.time()

##################### HEAD #######################

import os
import csv

import plotly.plotly as py
from plotly.graph_objs import *
from plotly.grid_objs import Column, Grid

#################### CONFIG ######################

base_directory = r"Downloads"

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

        reader = csv.DictReader(open(filename))
        for row in reader:
            column.append(row[column_name].strip())

        columns.append(column)
    
    return columns


def get_title(filename):

    if filename.endswith(".csv") or filename.endswith(".tsv"):
        filename = filename[:-4]
        return filename.replace("-", " ").title()

    else:
        return filename.replace("-", " ").title()


# makes the Plotly Grid object with the columns and the title
def make_grid(columns, filename):

    # list comprehension to create a list of Column objects used to make Grid
    # get_title gets the capitalized title for csv file    
    column_data = [Column(column, column_names[i]) for i, column in enumerate(columns)]
    grid = Grid(column_data)
    title = get_title(filename)

    return grid, title


##################### MAIN #######################


list_of_filenames = get_filenames(base_directory)
for filename in list_of_filenames:
    print filename
quit()

for filename in list_of_filenames:

    # open the csv first to get the column_names to use csv as dictreader
    file = open(filename)

    column_names = csv.reader(file).next()
    column_names = [column_name.strip() for column_name in column_names]
    columns = extract_column_data(filename, column_names)    

    grid, title = make_grid(columns, filename)
    grid_url = py.grid_ops.upload(grid, title, world_readable=True, auto_open=False)


##################### TIME #######################

print "Done!"
print "%s seconds" % (time.time() - start_time)
