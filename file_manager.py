# -*- coding: utf-8 -*-
import dedupe
import re
import csv
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
        with open(self.filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = [(k, self.preProcess(v)) for (k, v) in row.items()]
                row_id = int(row['Id'])
                self.data_dict[row_id] = dict(clean_row)
    
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

        pass
        
        


