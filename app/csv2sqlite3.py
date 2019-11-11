import csv
import re
import sqlite3
import sys

conn = sqlite3.connect('ARCSLiterature.sqlite3')
cursor = conn.cursor()


def doi_to_kw():
    with open('doi_keywords.csv', 'r') as keywordfile:
        data = csv.DictReader(keywordfile, delimiter=',', quotechar='"')
        doi_kwdict = {}
        for row in data:
            doi_kwdict[row['DOI']] = row['Author Keywords']
        return doi_kwdict

dictionary = doi_to_kw()


def getkeywords(DOI, dictionary):
    try:
        return dictionary[DOI]
    
    except KeyError:
        return ""
        


def parsecsv():
    with open('ARCSLiterature.csv', 'r') as thefile:
        data = csv.DictReader(thefile, delimiter=',', quotechar='"')
        datadict = {}
        for row in data:
            if row['Title'] not in datadict:
                datadict[row['Title']] = [row['Author'],
                                          row['Publication Year'],
                                          row['Publication Title'],
                                          row['Issue'],
                                          row['Volume'],
                                          row['DOI'],
                                          row['Abstract Note'],
                                          row['Manual Tags'],
                                          getkeywords(row['DOI'], dictionary)
                                          ]

            else:
                continue
        return datadict 

def createdatabase(datadict):
    try:
        cursor.execute('''CREATE TABLE bibliography(id INTEGER PRIMARY KEY,\
                   Title TEXT UNIQUE, Author TEXT, Year INTEGER, Source TEXT,\
                   Issue INTEGER, Volume INTEGER, DOI TEXT, Abstract TEXT,\
                   ManualTags TEXT, AuthorKeywords TEXT);''')
    except sqlite3.OperationalError:
        print("File already exists, remove it first")
        sys.exit()
    
    for k, v in datadict.items():
        try:
            cursor.execute('''INSERT INTO bibliography(Title, Author, Year, 
                          Source, Issue, Volume, DOI, Abstract, ManualTags, AuthorKeywords)
                          VALUES(?,?,?,?,?,?,?,?,?,?)''',
                          (k.title(), v[0], v[1], v[2].title(), v[3], 
                          v[4], v[5], v[6], v[7], v[8]))
        except sqlite3.IntegrityError:
            print("Found duplicate... continuing")
            continue
                          
    conn.commit()

createdatabase(parsecsv())




