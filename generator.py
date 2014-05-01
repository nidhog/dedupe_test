# -*- coding: utf-8 -*-
import json
import urllib2
from file_manager import FileManager

api_key = 'bddc358f620ef37a0b1ce6e6c46ef6c4ba168563'
url = 'https://api.locu.com/v1_0/venue/search/?'
json_obj = urllib2.urlopen(url+'&api_key='+api_key)

class Generator(object):
    def __init__(self):
        self.data = json.load(json_obj)
        
    def generate_data(self, filename):
        print "# # Generating data..."
        for datum in self.data['objects']:
            print '-'*40
            print " "*10,datum["name"]
            print '-'*40
            print "- Addresse: ",datum["street_address"]," CP:",datum["postal_code"]
            print "- Phone   : (+33) ",datum["phone"]
            
        print "# # Writing data on : '",filename, "' ..."
        f = FileManager(filename, 'w')
        f.make_file(self.data)
        
