# -*- coding: utf-8 -*-
import dedupe
import re
import csv

class FileManager(object):
    def __init__(self, filename):
        self.filename  = filename
        self.data_dict = {}
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
        


