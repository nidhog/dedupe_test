# -*- coding: utf-8 -*-
import numpy as npy

def compare(field1, field2):
    if field1 and field2 :
        if field1 == field2 :
            return 1
        else:
            return 0
    else :
        return npy.nan


file_name = {
            'input'   :'input_data.csv',
            'output'  :'output_data.csv',
            'setting' :'settings',
            'training':'training_features.json'
            }
            
fields = {
        'name': {'type': 'String'},
        }