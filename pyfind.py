import glob
import os
import argparse
import sys
import time

parser = argparse.ArgumentParser(
    prog="pyfind",
    description="Essentially a python version of the linux find command",
    epilog="",
)
parser.add_argument("glob")
parser.add_argument("-d", "--depth", default=-1)
args = parser.parse_args()


class Iterate:
    def __init__(self, glob_pattern, path=None):
        if path is None:
            path = os.curdir
        self.path = path
        self.current_depth = 0
        self.result = []
        self.glob_pattern = glob_pattern
        args.depth = int(args.depth)

    def check_if_can_return_results(self, path):
        if path == self.path:
            return True
        else:
            return False

    def iterate(self, path=None):
        if path is None:
            path = self.path
        print(f"\riterating on: {path}", end="", flush=True)
        ospath = os.path.normpath(path)
        paths = ospath.split(os.sep)
        if args.depth >= 0:
            if len(paths) < args.depth:
                pass
            else:
                return
        else:
            pass
        try:
            subdirs = [f.path for f in os.scandir(path) if f.is_dir()]
            for file in glob.glob(self.glob_pattern, root_dir=path):
                self.result.append(file)
            if len(subdirs) > 0:
                for subdir in subdirs:
                    self.iterate(subdir)

                if self.check_if_can_return_results(path):
                    return self.result
        except PermissionError:
            print(f"\raccess denied to \"{path}\" try running pyfind as admin\n")
            time.sleep(1)


if __name__ == "__main__":
    try:
        i = Iterate(args.glob, os.curdir)
        print(*i.iterate(), sep="\n")
    except KeyboardInterrupt:
        quit()
