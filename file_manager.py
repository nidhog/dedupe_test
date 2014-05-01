# -*- coding: utf-8 -*-
import dedupe
import re
import csv
import os
import collections

class FileManager(object):
    def __init__(self, filename, l='r'):
        self.filename  = filename
        self.data_dict = {}
        if(l=='r'):
            self.readFile()
        
    def readFile(self):
        """
        """
        try:
            with open(self.filename) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    clean_row = [(k, self.preProcess(v)) for (k, v) in row.items()]
                    row_id = int(row['Id'])
                    self.data_dict[row_id] = dict(clean_row)
        except:
            print "|!| Problem occured while trying to read the file : ", self.filename
            print ">   Make sure the file wasn't instatiated with 'r' if your purpose was not to read."
        
    def preProcess(self, column):
        """
        """
        column = dedupe.asciiDammit(column)
        column = re.sub('  +', ' ', column)
        column = re.sub('\n', ' ', column)
        column = column.strip().strip('"').strip("'").lower().strip()
        return column
        
    def setDict(self,new_dict):
        self.data_dict = new_dict

    def out(self, input_file, clustered_dupes):
        cluster_membership = collections.defaultdict(lambda : 'x')
        for (cluster_id, cluster) in enumerate(clustered_dupes):
            for record_id in cluster:
                cluster_membership[record_id] = cluster_id
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            with open(input_file) as f_input :
                reader = csv.reader(f_input)
                heading_row = reader.next()
                heading_row.insert(0, 'Cluster ID')
                writer.writerow(heading_row)
        
                for row in reader:
                    row_id = int(row[0])
                    cluster_id = cluster_membership[row_id]
                    row.insert(0, cluster_id)
                    writer.writerow(row)

    def make_file(self, data, header0='Id', header1='name'):
        if not(os.path.exists(self.filename)):
            with open(self.filename, 'w') as f:
                writer = csv.writer(f)
                heading_row = header0,header1
                writer.writerow(heading_row)
                i = 0
                for datum in data['objects']:
                    i+=1
                    row = i,datum["name"]
                    writer.writerow(row)
                    dummyname = datum["name"]
                    for j in xrange(len(dummyname)):
                        i+=1
                        drow = i, dummyname[:j]+str(j)+dummyname+dummyname[j:]
                        writer.writerow(drow)
        else:
            print "File with name: '", self.filename, "' Already exists."
        
        


