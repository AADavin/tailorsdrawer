import os
import sys

def careful_copy(inpath, outpath, extension):

    mfiles1 = {x for x in os.listdir(inpath) if x.endswith(extension)}
    mfiles2 = {x for x in os.listdir(outpath) if x.endswith(extension)}

    for mfile in (mfiles1 - mfiles2):
        print("cp %s %s" % ((os.path.join(inpath, mfile), os.path.join(outpath, mfile))))


args = sys.argv
if len(args) == 1:
    print("Usage: python careful_copy.py inpath outpath extension")
else:
    _, inpath, outpath, extension = args
    careful_copy(inpath, outpath, extension)




