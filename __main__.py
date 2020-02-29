from .reader import Reader
from .reader import Fmt
import sys
from datetime import datetime as dt


def main():
    if len(sys.argv) != 3:
        print('Usage: python -m thoughts <command> <arg>')
        return

    if sys.argv[1] == 'read':
        rdr = Reader(sys.argv[2])

        dt_birth = dt.fromtimestamp(rdr.birth)
        print(Fmt.USR.format(rdr.id, rdr.name, dt_birth, rdr.gender))

        for sn in rdr:
            snap_time = dt.fromtimestamp(sn.time / 1000)
            print(Fmt.SNPT.format(snap_time, sn.tx, sn.ty, sn.tz,
                                  sn.rx, sn.ry, sn.rz, sn.rw,
                                  sn.cwidth, sn.chight,
                                  sn.dwidth, sn.dhight))


if __name__ == '__main__':
    main()
