

import scipy.io
import numpy as np
import json

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from sigmf import sigmffile, utils
from sigmf.sigmffile import SigMFFile


class SigMF_matlab:
    
    def __init__(self):
        pass

    def create_sigmf_metafile(self, x_len, dest_data_filename):
        sigmf_md = SigMFFile(data_file = dest_data_filename)  
        sigmf_md.set_global_field("core:datatype", 'cf32')        
        sigmf_md.set_global_field("core:sample_rate", 5000000)        
        sigmf_md.set_global_field("core:author", 'Kunal Sankhe')
        sigmf_md.set_global_field("core:description", 'SigMF recording collected in indoor environment of ISEC, Northeastern University with distance of 2ft between transmitter and receiver.')
        sha =  sigmf_md.calculate_hash()
        print sha
        start_index = 0
        capture_len = x_len
        capture_md = {"core:time": utils.get_sigmf_iso8601_datetime_now(), "frequency":915000000}
        sigmf_md.add_capture(start_index=start_index, metadata=capture_md)
#         annotation_md = {
#             "core:latitude": 40.0 + 0.0001 * 0,
#             "core:longitude": -105.0 + 0.0001 * 0,
#         }

        sigmf_md.add_annotation(start_index=start_index,length=capture_len)

        return sigmf_md


    def create_sigmf_datafile(self):
        source_filepath = '/media/kunal/GENESYS-HD/INFOCOM2019-ORACLE-Dataset/KRI-16Devices-RawData/'
        dest_filepath = '/media/kunal/GENESYS-HD/INFOCOM2019-ORACLE-Dataset/SigMF-Dataset/KRI-16Devices-RawData/' 
        if not os.path.exists(dest_filepath):
            os.makedirs(dest_filepath)
        included_extensions = ['mat']
        file_names = [fn for fn in os.listdir(source_filepath)
                      if any(fn.endswith(ext) for ext in included_extensions)]

        for _file in file_names:
            print _file
            source_file = source_filepath + _file 
            print _file
            mat = scipy.io.loadmat(source_file)
            wifi_rx_data = mat['wifi_rx_data']
            x_len = len(wifi_rx_data)
            print x_len
            print wifi_rx_data[0]
            x_real = np.float32(np.real(wifi_rx_data))
            x_imag = np.float32(np.imag(wifi_rx_data))    
            x = np.zeros((x_len,2))
            x[:,0] = x_real.ravel()
            x[:,1] = x_imag.ravel()
            x = x.flatten()

            dest_data_filename = dest_filepath + _file[:-4] + '.sigmf-data'
            print dest_data_filename
            newFile = open(dest_data_filename, "wb")

            newFileByteArray = bytearray(x)
            newFile.write(newFileByteArray)

            #-------SigMF meta file------------------------

            sigmf_md = self.create_sigmf_metafile(x_len, dest_data_filename ) 
            

            print sigmf_md
            
            dest_meta_filename = dest_filepath + _file[:-4] + '.sigmf-meta'
            print dest_meta_filename
            #newFile = open(dest_meta_filename, "wb")
            
            with open(dest_meta_filename, 'w') as outfile:
                json.dump(sigmf_md.__dict__, outfile)


            break
        
        
def main():
    print "hello world!"
    x = SigMF_matlab()
    print "Hello"
    x.create_sigmf_datafile()
        
    
if __name__== "__main__":
    main()

    
    
    
