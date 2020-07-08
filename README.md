# Signal Metadata Format (SigMF)

Welcome to the GENESYS SigMF project! The SigMF specification document is the
`sigmf-spec.md` file in this repository:

SigMF: [Signal Metadata Format Specification](sigmf-spec.md)

According to SigMF specification, each recording must consist of two files: a metadata file and a dataset file. The dataset file is a binary file of digital samples, and the metadata file contains information that describes the dataset. Our metadata and data format is an extension of, and compatible with the SigMF specifications. For more information on the extension of SigMF, please refer a section 'Dataset Description' on the link http://www.genesys-lab.org/oracle.

## Introduction

Sharing sets of recorded signal data is an important part of science and
engineering. It enables multiple parties to collaborate, is often a necessary
part of reproducing scientific results (a requirement of scientific rigor), and
enables sharing data with those who do not have direct access to the equipment
required to capture it.

Unfortunately, these datasets have historically not been very portable, and
there is not an agreed upon method of sharing metadata descriptions of the
recorded data itself. This is the problem that SigMF solves.

By providing a standard way to describe data recordings, SigMF facilitates the
sharing of data, prevents the "bitrot" of datasets wherein details of the
capture are lost over time, and makes it possible for different tools to operate
on the same dataset, thus enabling data portability between tools and workflows.

(Taken from the
[Introduction](https://github.com/gnuradio/SigMF/blob/master/sigmf-spec.md#introduction)
of the specification document.)

## Scripts to convert your dataset stored in .mat (MATLAB supported files) into SigMF dataset

Step 1: Clone the repository

git clone https://github.com/kunalsankhe/Genesys-SigMF.git

## Run below commands

cd path-to-repository

cd Genesys-SigMF/tests

Modify variable annotation_md in mat2sigmf.py file according to your need. 

annotation_md = {
            "genesys:transmitter":{"antenna": {"model": "Ettus VERT2450", "type": "Vertical", "gain":3, "high_frequency":2480000000, "low_frequency":2400000000 }, "model": "Ettus USRP X310 with UBX-160 (10 MHz-6 GHz, 160 MHz BW) Daughterboard" },
            "genesys:reciever":{"antenna": {"model": "Ettus VERT2450", "type": "Vertical", "gain":3, "high_frequency":2480000000, "low_frequency":2400000000 }, "model": "Ettus USRP B210" }
        }


Run mat2sigmf.py by providing necessary input arguments.. Run --help to see required arguments.  
For example, 

python mat2sigmf.py --datatype cf32 --sample_rate 5000000 --source_filepath '/home/kunal/Temp/' --dest_filepath /home/kunal/Temp/SigMF/ --skip_datafile False --version 0.02

