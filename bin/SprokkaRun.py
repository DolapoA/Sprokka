#!/usr/bin/env python2.7

import sys
import os
import multiprocessing
import subprocess

# Get folder directory to analyse data
try:
    dataPath=sys.argv[1]
    run_Name=os.path.basename(dataPath)

    trim_ans=raw_input("\n## Note that you should keep a raw dataset aside before proceeding ##\n\nEnter 'y' to begin analysis:\n")
    roary_ans=raw_input("\nEnter 'y' to run roary:\n")
## Get number of cores to use from the user ##
    all_cores = multiprocessing.cpu_count()
    ncpus = raw_input("\nThis PC has " + str(all_cores) + ". Don't use too many cores because for every core you give, SPAdes needs 4.\nPlease enter n.o of cores: \n")

# Added in case user appends path to data with '/'
    if run_Name=="":
	    dataPath=dataPath[:-1]
	    run_Name=os.path.basename(dataPath)

# Get path of current script
    sprokkaPath=os.path.dirname(os.path.realpath(__file__))
    resultsPath=os.path.join(sprokkaPath.replace("bin", "results"), run_Name)
    roaryPath=os.path.join(resultsPath, "roary")
    roaryresultPath=os.path.join(roaryPath, "roary_result")

    try:
        os.makedirs(resultsPath, 0o777)
    except:
	    pass
    try:
		os.makedirs(roaryPath, 0o777)
    except:
		pass
    try:
		os.makedirs(roaryresultPath, 0o777)
    except:
		pass

    def data_prep():
    	print("\nTrimming raw fastq files in: " + dataPath)
    	print("\n")
    	os.chdir(dataPath)
    	for i in os.listdir(dataPath):
    		sampleID, filetype=i.split('_')
    		adapter="/opt/Trimmomatic-0.36/adapters/TruSeq3-PE.fa"
    		R1=(sampleID+"_R1.fastq.gz")
    		R2=(sampleID+"_R2.fastq.gz")
    		R1P=(sampleID+"_P_R1.fastq.gz")
    		R1U=(sampleID+"_U_R1.fastq.gz")
    		R2P=(sampleID+"_P_R2.fastq.gz")
    		R2U=(sampleID+"_U_R2.fastq.gz")

    		prep_command=" ".join(["java -jar /opt/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads 16", R1, R2, R1P, R1U, R2P, R2U, "".join(["ILLUMINACLIP:", adapter, ":2:30:10"]), "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"])
    		subprocess.check_call(prep_command, shell=True)
        
        for i in os.listdir(dataPath):
        	if '_U_' in i:
        		os.remove(i)

    def the_pipe():
	    print("\nRunning Sprokka pipe for samples in directory: " + dataPath)
	    print("\n")
	    os.chdir(dataPath)
	    pipe_command=" ".join(["ls *_R1.fastq.gz  | parallel -r -j", str(ncpus), os.path.join(sprokkaPath, "SprokkaProc.py"), dataPath, resultsPath, "{}"])
	    try:
	        subprocess.check_call(pipe_command, shell=True)
	    except:
	    	pass

    def run_Roary():
	    print("\nRunning Roary to create pan-genome. \n")
	    os.chdir(roaryPath)
	    roary_command=" ".join(["roary -f", roaryresultPath, "*.gff"])
	    try:
		    subprocess.check_call(roary_command, shell=True)
	    except:
		    pass

except:
	print("\nRun as follows: \n")
	print("python /path/to/SprokkaRun.py </path/to/data>")


if 'y' in trim_ans:
    data_prep()
    the_pipe()
if 'y' in roary_ans:
    run_Roary()
print("\n Done! ^_^ \n")
