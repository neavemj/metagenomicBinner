#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Calculate the coverage of metagenomic contigs using Bowtie2 and BedTools
Matthew J. Neave 7.5.15

"""
from __future__ import absolute_import
from __future__ import print_function

import argparse
import subprocess
import os
import sys
from six.moves import range


# use argparse to get fastq files and assembly file

parser = argparse.ArgumentParser("calculate average coverage of each contig in a metagenomic assembly")
parser.add_argument('assembly_file', type=str,
                    nargs=1, help="metagenomic assembly fasta file")
parser.add_argument('--fastq_files', '-f', type=str,
                    nargs="+", help="forward and reverse fastq files. "
                                    "Paired files should be given one after the other,"
                                    " e.g., sample1_R1.fq, sample1_R2.fq, etc.")
parser.add_argument('--threads', '-t', type=int, default=1,
                    nargs=1, help="number of threads for bowtie (default: 1)")
args = parser.parse_args()


# check that bowtie2 and bedtools are available in the path

def progAvail(*args):
    for prog in args:
        try:
            with open(os.devnull, 'w') as quiet:
                subprocess.call(prog, stdout=quiet, stderr=quiet)
        except OSError:
            print("error: couldn't find %s in your path" % prog)
            sys.exit(1)

progAvail("bowtie2", "bedtools", "samtools")


# create bowtie2 reference of the assembly

if args.assembly_file:
    assemb = args.assembly_file[0]
    index_name = assemb.split("/")[-1].split(".")[0]
    print("\n*** creating bowtie2 index ***")
    subprocess.call(["bowtie2-build", assemb, index_name])
else:
    print("metagenomic assembly file not found")
    sys.exit(1)


# map fastq files to the assembly, then calculate coverage with samtools and bedtools

def mapFastqCalcCov(fastq_1, fastq_2, name):
    if type(args.threads) is list:          # argparse returns list if args given but int if default value!! weird.
        threads = args.threads[0]
    else:
        threads = args.threads
    print("\n*** mapping %s files to the assembly ***\n" % name)
    subprocess.call(["bowtie2", "-p", str(threads), "-x", index_name, "-1", fastq_1, "-2",
                     fastq_2, "-S", name + ".sam"])

    # use samtools to sort and index sam mapping file
    print("\n*** converting sam to bam ***\n")
    subprocess.call(["samtools", "view", "-bS", name + ".sam", "-o", name + ".bam"])
    subprocess.call(["samtools", "sort", name + ".bam", name + ".sorted"])

    # calculate coverage per contig with bedtools
    # TODO: convert the bedtools output to ave cov per contig
    print("\n*** calculating coverage with bedtools ***\n")
    bedtools_coverage_file = open(name + ".bed_coverage.txt", "w")
    subprocess.call(["genomeCoverageBed", "-ibam", name + ".sorted.bam"],
                    stdout=bedtools_coverage_file)
    bedtools_coverage_file.close()


# loop through each library provided, map reads and calculate coverage
# the range bit means start at 0, end at max number of files, step by 2

library_num = 0
for i in range(0, len(args.fastq_files), 2):
    fq_1 = args.fastq_files[i]
    fq_2 = args.fastq_files[i+1]
    library_num += 1
    library = index_name + ".library_" + str(library_num)
    mapFastqCalcCov(fq_1, fq_2, name=library)

