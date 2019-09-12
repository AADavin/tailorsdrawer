import os

#mcom = "/home/uqadavin/Bin/iqtree-1.6.11-Linux/bin/iqtree -m TEST -s /90days/uqadavin/All/fam -bb 10000 -wbtl -nt AUTO -ntmax 6 -madd LG4X,LG4M,LG+C10,LG+C20,LG+C30,LG+C40,LG+C50,LG+C60,C10,C20,C30,C40,C50,C60"
mcom = "/home/uqadavin/Bin/iqtree-1.6.11-Linux/bin/iqtree -m TEST -s /90days/uqadavin/All/fam -bb 10000 -wbtl -nt AUTO -ntmax 6 -madd LG+C10"

mfams = [x for x in os.listdir("./") if ("filtered" in x and "filtered." not in x) or ("trimmed" in x and "trimmed." not in x)]

boots = {x for x in os.listdir("./") if "ufboot" in x}
finished = [x for x in mfams]

for fam in mfams:
    if fam + ".ufboot" in boots:
        pass
    else:
        print(mcom.replace("fam", fam))
