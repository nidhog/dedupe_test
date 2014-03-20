#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import re
import collections
import logging
import optparse
from numpy import nan

import dedupe
import json
import urllib2
import time
import dedupe

# Setup
input_file    = 'data.csv'
output_file   = 'output.csv'
settings_file = 'settings'
training_file = 'training.json'

api_key = 'bddc358f620ef37a0b1ce6e6c46ef6c4ba168563'
url = 'https://api.locu.com/v1_0/venue/search/?'
json_obj = urllib2.urlopen(url+'&api_key='+api_key)
data = json.load(json_obj)

print 'Number of businesses found :',len(data['objects'])

time.sleep(.5)
for datum in data['objects']:
    print '-'*40
    print " "*10,datum["name"]
    print '-'*40
    print "- Addresse: ",datum["street_address"]," CP:",datum["postal_code"]
    print "- Phone   : (+33) ",datum["phone"]
    time.sleep(.1)

print 'writing data on ',input_file,'...'
with open(input_file, 'w') as f:
    writer = csv.writer(f)
    header0 = 'Id'
    header1 = 'name'
    heading_row = header0,header1
    writer.writerow(heading_row)
    i = 0
    for datum in data['objects']:
        row_id = str(i)
        i+=1
        row = i,datum["name"]
        writer.writerow(row)
        dummyname = datum["name"]
        for j in xrange(len(dummyname)):
            i+=1
            drow = i, dummyname[:j]+str(j)+dummyname+dummyname[j:]
            writer.writerow(drow)

# Importing the data
def preProcess(column):
    column = dedupe.asciiDammit(column)
    column = re.sub('\n', ' ', column)
    column = re.sub('-', '', column)
    column = re.sub('/', ' ', column)
    column = re.sub("'", '', column)
    column = re.sub(",", '', column)
    column = re.sub(":", ' ', column)
    column = re.sub('  +', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    return column


def readData(filename):
    data_d = {}
    with open(filename) as input_source:
        reader = csv.DictReader(input_source)
        for line in reader:
            record = [(k, preProcess(v)) for (k, v) in line.items()]
            record_id = int(line['Id'])
            data_d[record_id] = dict(record)

    return data_d


print 'Reading and preprocessing...'
data_d = readData(input_file)

# Training
# In case some training settings already exist
if os.path.exists(settings_file):
    print 'Reading existing settings from', settings_file
    deduper = dedupe.StaticDedupe(settings_file)

else:
    # Define the fields and create a deduper object
    fields = {
        'name': {'type': 'String'},
        }

    deduper = dedupe.Dedupe(fields)

    # Train with a sample of records
    deduper.sample(data_d, 150000)


    # Train from saved data, if appropriate
    if os.path.exists(training_file):
        print 'Reading saved training examples from: ', training_file,'...'
        deduper.readTraining(training_file)

    # Start active learning 
    print 'Active learning started...'
    dedupe.consoleLabel(deduper)
    deduper.train()

    # Save training in training_file
    deduper.writeTraining(training_file)

    # Save settings in settings_file
    deduper.writeSettings(settings_file)


# Find appropriate threshold for precision/recall
threshold = deduper.threshold(data_d, recall_weight=2)

# Start clustering
print 'Clustering started...'
clustered_dupes = deduper.match(data_d, threshold)

print '-->   Clustered dupes : ', len(clustered_dupes)
print '- * Output data has been exported to :',output_file,' * -'

# saving the output in output_file
collection = collections.defaultdict(lambda : 'x')
for (dupe_id, cluster) in enumerate(clustered_dupes):
    for record_id in cluster:
        collection[record_id] = dupe_id

with open(output_file, 'w') as f:
    writer = csv.writer(f)

    with open(input_file) as f_input :
        reader = csv.reader(f_input)

        heading_row = reader.next()
        heading_row.insert(0, 'Cluster ID')
        writer.writerow(heading_row)

        for row in reader:
            row_id = int(row[0])
            dupe_id = collection[row_id]
            row.insert(0, dupe_id)
            writer.writerow(row)
