import os
import sys
from drawer import fasta_parser

args = sys.argv
if len(args) == 0:
    print("Usage: python prepare_triplets.py inpath outpath")
else:
    _, path_folder_with_triplets, outpath = args
    mold = ("(A1,A2,A3);")
    triplets = [x for x in os.listdir(path_folder_with_triplets) if x.endswith("faa")]

    for triplet in triplets:
        mnames = list()
        for h,_ in fasta_parser(os.path.join(path_folder_with_triplets, triplet)):
                mnames.append(h)

        h1, h2, h3 = tuple(mnames)

        mtriplet = mold.replace("A1",h1).replace("A2",h2).replace("A3",h3)
        with open(os.path.join(outpath, triplet + ".nwk"), "w") as f:
            f.write(mtriplet)



