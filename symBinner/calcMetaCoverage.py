#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Calculate the coverage of metagenomic contigs using Bowtie2 and BedTools
Matthew J. Neave 7.5.15

"""

import argparse
import subprocess
import os
import sys

# use argparse to get fastq files and assembly file

parser = argparse.ArgumentParser("calculate average coverage of each contig in a metagenomic assembly")

parser.add_argument('fastq_files', type=str,
                    nargs=2, help="forward and reverse fastq files")
parser.add_argument('assembly_file', type = str,
                    nargs=1, help="metagenomic assembly fasta file")
parser.add_argument('--threads', '-t', type = int,
                    nargs="?", help="number of threads for bowtie (default: 1)",
                    default=1)

args = parser.parse_args()

# check that bowtie2 and bedtools are available in the path

def progAvail(*args):
    for prog in args:
        try:
            with open(os.devnull, 'w') as quiet:
                subprocess.call(prog, stdout=quiet, stderr=quiet)
        except OSError:
            print "error: couldn't find %s in your path" % prog
            sys.exit(1)

progAvail("bowtie2", "bedtools", "samtools")

# create bowtie2 reference of the assembly

if args.assembly_file:
    assemb = args.assembly_file[0]
    index_name = assemb.split("/")[-1]
    print "\n*** creating bowtie2 index ***"
    #subprocess.call(["bowtie2-build", assemb, index_name])
else:
    print "metagenomic assembly file not found"
    sys.exit(1)

# map fastq files to the assembly

if args.fastq_files:
    threads = args.threads
    fastq1 = args.fastq_files[0]
    fastq2 = args.fastq_files[1]
    print "\n*** mapping fastq files to the assembly ***"
    #subprocess.call(["bowtie2", "-p", str(threads), "-x", index_name, "-1", fastq1, "-2", fastq2,
     #                "-S", index_name + ".sam"])
else:
    print "fastq files not found"
    sys.exit(1)

# use samtools to sort and index sam mapping file

print "\n*** converting sam to bam ***"
input_sam = index_name + ".sam"
output_bam = index_name + ".bam"
#subprocess.call(["samtools", "view", "-bS", input_sam, "-o", output_bam])
#subprocess.call(["samtools", "sort", output_bam, index_name + ".sorted"])

print "\n*** calculating coverage with bedtools ***"

bedtools_coverage_file = open("bed_coverage.txt", "w")
subprocess.call(["genomeCoverageBed", "-ibam", index_name + ".sorted.bam"],
                stdout=bedtools_coverage_file)
bedtools_coverage_file.close()



