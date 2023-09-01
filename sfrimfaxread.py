import argparse
import os.path
import sys

from cdr import cdr


def cli():
    parser = argparse.ArgumentParser(description="Convert RIMFAX CDR Files to RSF")
    parser.add_argument("files", type=str, nargs="+", help="XML label(s) of file(s) to convert")
    parser.add_argument("-p", "--progress_bar", action="store_true", help="Display progress bars")
    return parser.parse_args()


def main():
    args = cli()
    for file in args.files:
        # Check if file exists
        if not os.path.isfile(file):
            sys.stderr.write("%s does not exist, skipping\n" % file)
            continue

        # Check if file is xml
        name, ext = os.path.splitext(file)
        if ext.lower() != ".xml":
            sys.stderr.write("%s extension is not .xml, skipping\n" % file)

        # Open and write out RSF
        rfax = cdr(file, progress_bar=args.progress_bar)
        rfax.writeRSF(progress_bar=args.progress_bar)


if __name__ == '__main__':
    main()