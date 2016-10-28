##################### HEAD #######################

#Version 1.2

import requests
from selenium import webdriver
from lxml import html

import sys
import csv

#################### CONFIG ######################

debug = False
print_headers = False
path_to_chromedriver = "/Users/Admin/Desktop/chromedriver"

################### FUNCTIONS ####################


# Same as client load but much more lightweight
def load(url, headers = {}):

    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    if headers == -1:
        headers = None

    try:
        response = requests.get(url, headers = headers)

    except:
        print "[ERROR] Connection error."  
        quit()

    if debug:
        file = open("debug.html", 'w')
        file.write(response.content)
    if print_headers:
        print response.status_code # Response Code  
        print response.headers # Response Headers
        
    return response


# This function fetches the website and returns an html object
def client_load(url, client = None, headers = {}):


    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    if headers == -1:
        headers = None

    if not client:

        try:
            client = requests.Session()   
        except:
            print "[ERROR] Session Error."  

    try:
        response = client.get(url, headers = headers)

    except:
        print "[ERROR] Connection error."  
        quit()

    if debug:
        file = open("debug.html", 'w')
        file.write(response.content)
    if print_headers:
        print response.status_code # Response Code  
        print response.headers # Response Headers

    return response, client


# This function browses the web using Selenium
def browse(url, client = None, headers = {}):

    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} 

    try:
        browser = webdriver.Chrome(executable_path = path_to_chromedriver)
        response = browser.get(url)

    except:
        print "[ERROR] Connection error."
        quit()

    return response, client


# This function prints listings to console
def output_console(objects, fields):

    row_headers = [field.capitalize() for field in fields]

    print u"-" * 160

    print u"[##]  ",
    for i, column in enumerate(row_headers):  
        print u"{:32}    ".format(column[:32]), 
    print ""

    for i, obj in enumerate(objects):
        row = [getattr(obj, field) for field in fields]

        print u"[{:2}]  ".format(i+1),
        for column in row:
            print u"{:32}    ".format(column[:32]), 
        print "" 

    print "-" * 160


# This function exports listings as csv file
def output_csv(filename, objects, fields):

    if ".csv" not in filename: filename = filename + ".csv"

    row_headers = [field.capitalize() for field in fields]

    try :
        file = open(filename, "a")
        writer = csv.writer(file)
    except :
        file = open(filename, "w")
        write = csv.writer(file)
        writer.writerow(row_headers)

    for obj in objects:
        row = [getattr(obj, field) for field in fields]
        row = [column.encode('utf-8') for column in row]
        writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)
