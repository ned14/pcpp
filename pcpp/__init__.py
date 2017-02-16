from __future__ import absolute_import, print_function
import sys
from pcpp.pcpp import Preprocessor

def main():
    print("Still to implement command line edition")
    sys.exit(1)
    #if len(sys.argv)<3:
    #    print("Usage: "+sys.argv[0]+" outputpath [-Iincludepath...] [-Dmacro...] header1 [header2...]", file=sys.stderr)
    #    sys.exit(1)
    p = Preprocessor(quiet=False)
    with open(inpath, 'rt') as ih:
        p.add_raw_lines(ih.readlines(), path)
    p.preprocess()
    with open(outpath, 'w') as oh:
        oh.writelines(p.get_lines())
    sys.exit(p.return_code)
        
