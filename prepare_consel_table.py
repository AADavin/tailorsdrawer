import sys
import os


# Reads a directory with all reconciliations produced by ALE undaded and pulls out the family likelihoods and writes
# the output ready for Consel


args = sys.argv

if len(args) == 0:
    print("Usage: python prepare_consel_table.py yourdirwithreconciliations")

_, dir = args

recs_files = [x for x in os.listdir(dir) if x.endswith("uml_rec")]

trees = {x.split("_")[1]:set() for x in recs_files}

for rec in recs_files:
    h = rec.split("_")
    rec, fam = h[1], h[2]
    trees[rec].add(fam)

tt = set.intersection(trees)










