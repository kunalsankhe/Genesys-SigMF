"""
__author__: Kunal Sankhe
__website__: https://kunalsankhe.github.io/
__email__: sankhe.ku@northeastern.edu
"""

import argparse
#from utils.utilities import str2bool

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description = 'Recording in Signal Metadata Format (SigMF) with dataset and metafile',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Input dataset section
parser.add_argument('-d', '--datatype', default='cf32', required=True, help='The format of the stored samples in the dataset file. Its value must be a valid SigMF dataset format type string.')
parser.add_argument('-s', '--sample_rate', type =float, default=5000000, required=True, help='The sample rate of the signal in samples per second')
parser.add_argument('-f', '--frequency', type =float, default=2450000000, help='The frequency of the capture')
parser.add_argument('-a', '--author', default='Kunal Sankhe', help='The author\'s name')
parser.add_argument('--source_filepath', default='', help='Filepath of the .mat source file to be converted to SigMF')
parser.add_argument('--dest_filepath', default='', help='Filepath where SigMF data and meta files will be stored.')
parser.add_argument('--skip_datafile', default=False, type=str2bool, help='Skip datafile?')
parser.add_argument('-ds', '--description', default='', help='The description in metafile of the SigMF recordings')
parser.add_argument('--mat_variable', default='wifi_rx_data', help='MATLAB variable name that stores .mat data')

args = parser.parse_args()

param ={}
param['datatype'] =args.datatype
param['sample_rate'] =args.sample_rate
param['source_filepath'] =args.source_filepath
param['dest_filepath'] =args.dest_filepath
param['author'] =args.author
param['skip_datafile'] =args.skip_datafile
param['frequency'] = args.frequency
param['description'] = args.description
param['mat_variable'] = args.mat_variable

import scipy.io
import numpy as np
import json
import re


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from sigmf import sigmffile, utils
from sigmf.sigmffile import SigMFFile


class SigMF_matlab:
    
    def __init__(self, param):
    	self.source_filepath = param['source_filepath']
    	self.datatype = param['datatype']
    	self.dest_filepath = param['dest_filepath']
    	self.author =param['author']
    	self.sample_rate =param['sample_rate']
    	self.skip_datafile = param['skip_datafile']
    	self.frequency = param['frequency']
        self.description = param['description']
        self.mat_variable = param['mat_variable']
        #pass

    def create_sigmf_metafile(self, x_len, dest_data_filename, _file):        

        sigmf_md = SigMFFile(data_file = dest_data_filename)  
        sigmf_md.set_global_field("core:datatype", self.datatype)        
        sigmf_md.set_global_field("core:sample_rate", self.sample_rate)        
        sigmf_md.set_global_field("core:author", self.author)
        sigmf_md.set_global_field("core:description", self.description)
        sha =  sigmf_md.calculate_hash()
        print sha
        start_index = 0
        capture_len = x_len
        capture_md = {"core:time": utils.get_sigmf_iso8601_datetime_now(), "frequency":self.frequency}
        sigmf_md.add_capture(start_index=start_index, metadata=capture_md)
        
        annotation_md = { "genesys:transmitter":{"antenna": {"model": "Ettus VERT2450", "type": "Vertical", "gain":3, "high_frequency":2480000000, "low_frequency":2400000000 }, "model": "Ettus USRP X310 with UBX-160 (10 MHz-6 GHz, 160 MHz BW) Daughterboard" }, "genesys:reciever":{"antenna": {"model": "Ettus VERT2450", "type": "Vertical", "gain":3, "high_frequency":2480000000, "low_frequency":2400000000 }, "model": "Ettus USRP B210" } }
               
        sigmf_md.add_annotation(start_index=start_index,length=capture_len, metadata = annotation_md)
        return sigmf_md

    def create_directory(self, dir_path):
    	if not os.path.exists(dir_path):
            os.makedirs(dir_path)


    def create_sigmf_datafile(self):
        
        included_extensions = ['mat']
        file_names = [fn for fn in os.listdir(self.source_filepath)
                      if any(fn.endswith(ext) for ext in included_extensions)]
        for _file in file_names:
            print _file
            source_file = self.source_filepath + _file 
            mat = scipy.io.loadmat(source_file)                      
            wifi_rx_data = mat[self.mat_variable]            
            x_len = len(wifi_rx_data)                                    
            dir_filepath = self.dest_filepath
            print dir_filepath  
            dest_data_filename = dir_filepath  + _file[:-4] + '.sigmf-data'            
            print dest_data_filename

            if not os.path.exists(dir_filepath):
                os.makedirs(dir_filepath)

            if(not self.skip_datafile):
            	print "Creating SigMF datafile"
            	x_real = np.float32(np.real(wifi_rx_data))
            	x_imag = np.float32(np.imag(wifi_rx_data))
            	x = np.zeros((x_len,2), dtype = np.float32)
            	x[:,0] = x_real.ravel()
            	x[:,1] = x_imag.ravel()
            	x = x.flatten()            	
            	print dest_data_filename
            	newFile = open(dest_data_filename, "wb")
            	newFileByteArray = bytearray(x)
            	newFile.write(newFileByteArray)
            	print "Finished SigMF datafile"
            #-------SigMF meta file------------------------
            
            print "Creating SigMF metafile"

            sigmf_md = self.create_sigmf_metafile(x_len, dest_data_filename, _file )                                     
            dest_meta_filename = dir_filepath + _file[:-4] + '.sigmf-meta'
            print dest_meta_filename
            
            with open(dest_meta_filename, 'w') as outfile:
                json.dump(sigmf_md.__dict__, outfile)

            print "Finished SigMF datafile"
         
        
def main(param):
    x = SigMF_matlab(param)   
    x.create_sigmf_datafile()
    
if __name__== "__main__":	
    main(param)

    
    
    
