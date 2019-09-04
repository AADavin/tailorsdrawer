def fasta_parser(myfile):
    with open(myfile) as f:

        header = ""
        seq = ""
        for line in f:
            if line[0] == ">":
                if seq != "":
                    yield (header[1:], seq)
                    header = line.strip()
                    seq = ""
                else:
                    header = line.strip()
            else:
                seq += line.strip()
        yield (header[1:], seq)
