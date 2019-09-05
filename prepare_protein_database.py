from drawer import fasta_parser

import os
import sys

_, path = sys.argv

fasta_files = [x for x in os.listdir(path) if x.endswith(".faa")]

sp = 0
seq = 0


with open("./AllProteins.fasta", "w") as f1:
    with open("./Sp2Acc.txt", "w") as f2:
        with open("./Seq2Prod.txt", "w") as f3:
            for fasta_file in fasta_files:
                msp = "n" + str(sp)
                acc = fasta_file.replace("_gene.faa", "")
                line2 = "\t".join([msp, acc]) + "\n"
                f2.write(line2)
                for h, seq in fasta_parser(os.path.join(path, fasta_file)):
                    mseq = str(seq)
                    line1 = ">" + msp + "_" + mseq + "\n"
                    f1.write(line1)
                    f1.write(seq + "\n")
                    f3.write(msp + "_" + mseq + "\t" + h + "\n")
                    seq +=1
            sp += 1





