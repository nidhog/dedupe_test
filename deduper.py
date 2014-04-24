# -*- coding: utf-8 -*-

import dedupe
import os
import logging


logging.basicConfig()
moduleLogger = logging.getLogger('main')



class Deduper(object):
    def __init__(self, settings, fields):
        self.duper = None
        self.settings_used = False
        self.dupe(settings, fields)
        self.clusters = None
        #add Files?
        pass
    
    def dupe(self, settings, fields):
        print "Looking for settings..."
        if(self.try_settings(settings)):
            print "# # SETTINGS USED"
            self.settings_used = True
        else:
            self.duper = dedupe.Dedupe(fields)
            print "# # SETTINGS NOT USED. Used fields instead."
            
    def try_settings(self, settings):
        if os.path.exists(settings):
            self.duper = dedupe.StaticDedupe(settings)
            return True
        else:
            return False
            
    def train(self, data_sample, useTrainingFile = True, training_file = None, N=150000):
        if(not((self.settings_used) or (self.duper is None))):
            try:
                self.duper.sample(data_sample, N)
                if(useTrainingFile):
                    if os.path.exists(training_file):
                        print 'Reading labeled examples from ', training_file, '...'
                        self.duper.readTraining(training_file)
            except:
                print "|!| UNEXPECTED ERROR"
                raise
                    
    def start_active_labeling(self, training_file, settings):
        if(not(self.settings_used)):
            print 'Active Labeling...'
            dedupe.consoleLabel(self.duper)
            self.duper.train()
            self.duper.save(training_file, settings)
        
    def save(self, training_file, settings):
        self.duper.writeTraining(training_file)
        self.duper.writeSettings(settings)
        
    def start_clustering(self, data_sample, recall_weigth =2):
        print 'Computing the threshold...'
        threshold = self.duper.threshold(data_sample, recall_weigth)
        print 'Clustering...'
        self.clusters = self.duper.match(data_sample, threshold)
        print '# # CLUSTERING ENDED. Found ', len(self.clusters), ' clusters.'
        
        
    
