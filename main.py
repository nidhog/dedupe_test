# -*- coding: utf-8 -*-

from deduper import Deduper
from config import file_name, fields
from file_manager import FileManager

deduper = Deduper(file_name['setting'], fields)

data_file   = FileManager(file_name['input'])
data_sample = data_file.data_dict

deduper.train(data_sample, True, file_name['training'])

deduper.start_active_labeling(file_name['training'], file_name['setting'])

deduper.start_clustering(data_sample)

output_file = FileManager(file_name['output'],'w')
output_file.out(file_name['input'], deduper.clusters)