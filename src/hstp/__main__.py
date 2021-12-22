import argparse
import os

import hstp

def main():

    parser = argparse.ArgumentParser(
        prog='python -m hstp',
        description='Build an '
    )

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-i", "--input", help="input directory")
    parser.add_argument(
        "-o",
        "--output",
        help="output directory",
        default="../out")

    args = parser.parse_args()

    i = hstp.Info()

    if not args.input or (not os.path.isdir(args.input)):
        i.error("Input directory does not exist")
        exit(1)

    if not args.output or (not os.path.isdir(args.input)):
        i.error("Input directory does not exist")
        exit(1)

    r = hstp.Reader(i, args.input)
    r.load_podcasts()
    r.save(args.output)

if __name__ == "__main__":
    main()
