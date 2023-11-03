from base_refactory import BaseRefactory
from clean_mlcqcodesmellsamples import CleanMLCQ


if __name__ == '__main__':
    cmlcq: CleanMLCQ = CleanMLCQ("removidos.csv")
    cmlcq.run()
    BaseRefactory.run("ids.txt")
