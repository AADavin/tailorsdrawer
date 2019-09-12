import sys
import os
_, coms  = sys.argv

i = 0

with open("./" + coms) as f:
    for l in f:
        i+=1
        with open("./" + "x" + str(i), "w") as f:
            f.write(l.strip())
