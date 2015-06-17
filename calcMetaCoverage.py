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
import csv
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
    print("\n*** calculating coverage with bedtools ***\n")
    output = subprocess.Popen(["genomeCoverageBed", "-ibam", name + ".sorted.bam"], stdout=subprocess.PIPE)
    stdout, stderr = output.communicate()

    # create a contig list for later ordering of output
    contig_list = []
    for line in stdout.decode('ascii').splitlines():
        contig = line.split()[0]
        if contig not in contig_list:
            contig_list.append(contig)

    # use DictReader to create a dictionary of the bedtools output
    result_dict = csv.DictReader(stdout.decode('ascii').splitlines(), delimiter="\t",
       fieldnames=['contig', 'depth', 'eqDepth', 'size', 'per_depth'])

    # this calculates the coverage on a per contig basis
    cov_dict = {}
    for result in result_dict:
        contig = result['contig']
        depth = float(result['depth'])
        per_depth = float(result['per_depth'])
        if contig in cov_dict:
            cov_dict[contig] += depth * per_depth
        else:
            cov_dict[contig] = depth * per_depth

    # write using 'contig_list' to maintain contig ordering
    file_output = open(name + ".coverage", "w")
    for contig_name in contig_list:
        file_output.write(contig_name + "\t" + str(cov_dict[contig_name]) + "\n")

# loop through each library provided, map reads and calculate coverage
# the range bit means start at 0, end at max number of files, step by 2 for paired-end files

for i in range(0, len(args.fastq_files), 2):
    fq_1 = args.fastq_files[i]
    fq_2 = args.fastq_files[i+1]
    lib_name = fq_1.split("/")[-1].split(".")[0]
    library = index_name + "." + lib_name
    mapFastqCalcCov(fq_1, fq_2, name=library)

