#!/usr/bin/env python2.7


# Dolapo Ajayi, August 2018
# The purpose of this script (and SprokkaRun.py) is to automate the running of SPAdes, Prokka and Roary and to adequately organise the results.

import sys
import os
import glob
import subprocess
import shutil
from shutil import copyfile

# Collect arguments from SprokkaRun.py
dataPath=sys.argv[1]
resultsPath=sys.argv[2]
fastqR1=sys.argv[3]

# Change name #
fastqR2=fastqR1.replace("R1","R2")
# Get basename of path, then split for strain name #
b_name=os.path.basename(fastqR2)
strainName, filetype = b_name.split('_P_')

print("Running SPAdes for:  " + strainName)


## Create directories for each sample ##
strainDir=os.path.join(resultsPath, strainName)
roaryPath=os.path.join(resultsPath, "roary")

try:
    os.makedirs(strainDir, 0o777)
except:
    pass

def run_Spades():
    print("Running SPAdes \n")
    spadesDir=os.path.join(strainDir, "spades")
    file_list=[]
    for file in glob.glob(os.path.join(spadesDir,'*')):
        file=os.path.basename(file)
        file_list.append(file)

    if 'contigs.fasta' in file_list:
        print(" ".join(["SPAdes results for", strainName, "already obtained."]))
    else:
        print(" ".join(["Running SPAdes for", os.path.basename(fastqR1)]))        
        spades_command=" ".join(["spades -t 8 -k 21,33 --careful -1", os.path.join(dataPath, fastqR1), "-2", os.path.join(dataPath, fastqR2), "-o", spadesDir])
        try:
            subprocess.check_call(spades_command, shell=True)
        except:
            print("SPAdes has failed for "+strainName)
    return spadesDir


def run_Prokka(spadesDir):
    print("Running Prokka \n")
    prokkaDir=os.path.join(strainDir, "prokka")
    file_list=[]
    for file in glob.glob(os.path.join(prokkaDir, '*')):
        file=os.path.basename(file)
        file_list.append(file)

    if len(file_list)==11:
        print(" ".join(["Prokka results for", strainName, "already obtained." ]))
    else:
        print(" ".join(["Running Prokka for", strainName]))
        prokka_command=" ".join(["prokka --outdir", prokkaDir, "--genus 'Salmonella' --centre C --locustag L", os.path.join(spadesDir, "contigs.fasta")])
        try:
            subprocess.check_call(prokka_command, shell=True)
        except:
            print("Prokka has failed for "+strainName)

# Change name of result files into sample-based name
    os.chdir(prokkaDir)
    for f in os.listdir(prokkaDir):
        file=os.path.basename(f)
        filename, filetype=str(file).split('.')
        os.rename(f, ".".join([strainName, filetype]))

# Copy .gff files to roary results directory
    for f in os.listdir(prokkaDir):
        if '.gff' in f:
            try:
                shutil.copyfile(f, os.path.join(roaryPath, f))
            except:
                pass

run_Spades()
run_Prokka(run_Spades())
