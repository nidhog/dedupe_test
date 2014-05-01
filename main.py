#! /usr/bin/env python
# -*- coding: utf-8 -*-

from deduper import Deduper
from config import file_name, fields
from file_manager import FileManager
from generator import Generator

# Generate input data if it does not exist
input_generator = Generator()
input_generator.generate_data(file_name['input'])

# Create deduper
deduper = Deduper(file_name['setting'], fields)

# Get data dictionary
data_file   = FileManager(file_name['input'])
data_sample = data_file.data_dict

# Train
deduper.train(data_sample, True, file_name['training'])

# Active Labeling
deduper.start_active_labeling(file_name['training'], file_name['setting'])

# Clustering
deduper.start_clustering(data_sample)

# Writing output
output_file = FileManager(file_name['output'],'w')
output_file.out(file_name['input'], deduper.clusters)