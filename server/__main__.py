from pathlib import Path
from .server import run
import sys

def main(argv):
    if len(argv) != 3:
        print(f'TODO')
        return 1

    run(argv[1], argv[2])



if __name__ == '__main__':
    main(sys.argv)
