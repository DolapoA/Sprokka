### Sprokka ###


SprokkaRun and SprokkaProc are 2 scripts that form a mini-pipe for processing fasta sequences through SPAdes followed by Prokka.



## Installation:
Download and store Sprokka somewhere reasonable i.e. in /home/

Dependencies:
SPAdes - https://github.com/ablab/spades
https://www.ncbi.nlm.nih.gov/pubmed/22506599

Prokka - https://github.com/tseemann/prokka
Seemann T, "Prokka: Rapid Prokaryotic Genome Annotation", 
Bioinformatics, 2014 Jul 15;30(14):2068-9.


PMID:24642063
doi:10.1093/bioinformatics/btu153
http://www.ncbi.nlm.nih.gov/pubmed/24642063

GNU Parallel -https://www.gnu.org/software/parallel/
@book{tange_ole_2018_1146014,
      author       = {Tange, Ole},
      title        = {GNU Parallel 2018},
      publisher    = {Ole Tange},
      month        = Mar,
      year         = 2018,
      ISBN         = {9781387509881},
      doi          = {10.5281/zenodo.1146014},
      url          = {https://doi.org/10.5281/zenodo.1146014}
}

Trimmomatic - https://github.com/timflutre/trimmomatic
To prepare data for Sprokka

python2.7 - https://www.python.org/downloads/release/python-2714/

Optional: Roary - https://github.com/sanger-pathogens/Roary

## Your data:
Your data folder should contain both R1 and R2 fastq(.gz) files per sample.

## How to run it:
python /path/to/SprokkaRun.py </path/to/data_name>

## Your results:
Your results (as per sample) will be kept in the results folder of the main (Sprokka) directory
i.e. - ~/Sprokka/results/data_name/sample_1/spades/contigs.fasta
     - ~/Sprokka/results/data_name/sample_1/prokka/result.gff
     
     
# Dolapo Ajayi, August 2018 - Contact: dolaajayi@hotmail.com
