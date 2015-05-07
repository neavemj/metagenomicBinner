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
                    nargs = 2, help = "forward and reverse fastq files")
parser.add_argument('assembly_file', type = str,
                    nargs = 1, help = "metagenomic assembly fasta file")
parser.add_argument('--threads', '-t', type = int,
                    nargs = 1, help = "number of threads for bowtie (default: 1)")

args = parser.parse_args()

# check that bowtie2 and bedtools are available in the path

def progAvail(*args):
    for prog in args:
        try:
            with open(os.devnull, 'w') as quiet:
                subprocess.call(prog, stdout=quiet, stderr=quiet)
        except OSError:
            print "couldn't find %s in your path" % prog
            sys.exit(1)

progAvail("bowtie2", "bedtools")

# create bowtie2 reference of the assembly

if args.assembly_file:
    print "you have a file!"
else:
    print "metagenomic assembly file not given"