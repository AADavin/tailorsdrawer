import sys
import os


# Reads a directory with all reconciliations produced by ALE undaded and pulls out the family likelihoods and writes
# the output ready for Consel


args = sys.argv

if len(args) == 0:
    print("Usage: python prepare_consel_table.py yourdirwithreconciliations youroutpath ignorelessthan extension")
    print("For instance, prepare_consel_table.py recs outconsel 3000 .faa.aln.trimmed.ufboot.corrected.ale.uml_rec")

else:
    _, indir, outdir, minimum, extension = args

    def extract_ll(rec_file):
        with open(rec_file) as f:
            for l in f:
                if l.startswith(">logl"):
                    ll = l.split(":")[-1].strip()
                    return ll
    recs_files = [x for x in os.listdir(indir) if x.endswith("uml_rec")]
    trees = {x.split("_")[1]:set() for x in recs_files}
    for rec in recs_files:
        h = rec.split("_")
        rec, fam = h[1], h[2]
        fam = fam.split(".")[0]
        trees[rec].add(fam)
    mtrees = dict()
    for tree in trees:
        if len(trees[tree]) < int(minimum):
            continue
        else:
            mtrees[tree] = trees[tree]


    sharedrecs = set.intersection(*mtrees.values())
    sharedrecsordered = list(sharedrecs)

    with open(os.path.join(outdir, "likelihoods_table"), "w") as f:
        f.write("\t".join([str(len(trees)), str(len(sharedrecsordered))]) + "\n")
        for tree, fams in mtrees.items():
            head = list()
            line = list()
            head.append("#" + tree)
            for fam in sharedrecsordered:
                rec_file = os.path.join(indir, "SpeciesTree_TREE_FAM".replace("TREE", tree).replace("FAM",fam) + extension)
                line.append(extract_ll(rec_file))
            head = "".join(head) + "\n"
            line = " ".join(line) + "\n"
            f.write(head)
            f.write(line)






























