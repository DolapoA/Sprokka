#!/usr/bin/env python2.7


# Dolapo Ajayi, August 2018
# The purpose of this script (and SprokkaProc.py) is to automate the running of SPAdes and Prokka and to adequately organise the results.



import sys
import os
import multiprocessing
import subprocess

# Get folder directory to analyse data
try:
    dataPath=sys.argv[1]
    run_Name=os.path.basename(dataPath)
## Get number of cores to use from the user ##
    all_cores = multiprocessing.cpu_count()
    ncpus = raw_input("\nThis PC has " + str(all_cores) + ". Don't use too many cores because for every core you give, SPAdes needs 4.\nPlease enter n.o of cores: ")

# Added in case user appends path to data with '/'
    if run_Name=="":
	    dataPath=dataPath[:-1]
	    run_Name=os.path.basename(dataPath)

# Get path of current script
    sprokkaPath=os.path.dirname(os.path.realpath(__file__))
    resultsPath=os.path.join(sprokkaPath.replace("bin", "results"), run_Name)

    try:
        os.makedirs(resultsPath, 0o777)
    except:
	    pass

    def the_pipe():
	    print("\nRunning pipe for samples in directory: " + dataPath)
	    print("\n")
	    os.chdir(dataPath)
	    pipe_command=" ".join(["ls *_R1.fastq.gz  | parallel -r -j", str(ncpus), os.path.join(sprokkaPath, "SprokkaProc.py"), dataPath, resultsPath, "{}"])
	    try:
	        subprocess.check_call(pipe_command, shell=True)
	    except:
	    	pass
except:
	print("\nRun as follows: \n")
	print("python /path/to/SprokkaRun.py </path/to/data>")



try:
    the_pipe()
    print("\n Done! ^_^ \n")
except:
	pass

