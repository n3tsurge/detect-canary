import os
import sys
import zipfile
import glob
import logging
import argparse

def get_files(base_path=".", pattern="*.docx"):
    '''
    Use a base_path and a glob pattern to create a list
    of files we want to work on
    '''

    full_path = os.path.join(base_path,pattern)
    print(full_path)

    files = glob.glob(full_path)
    return files


if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="The base path where to search")
    parser.add_argument('--search', type=str, help="The pattern to search for e.g. *.docx", default="*.docx")
    parser.add_argument('--keywords', type=list, help="A list of keywords to look for that may indicate the file is a canary", default=['INCLUDEPICTURE'])

    args = parser.parse_args()
    if not args.path:
        logging.error("Need to supply a search path using the --path parameter")
        logging.error("Exiting...")
        sys.exit(1)

    # Create a list of files to work on
    files = get_files(args.path, args.search)

    logging.info("Found {} files".format(len(files)))
    # For each file, open the zip container and look
    # for a file named footer2.xml
    for f in files:
        logging.info("Working on \"{}\"".format(f))
        with zipfile.ZipFile(f) as z:
            footers = [m for m in z.namelist() if m.endswith('footer2.xml')]
            if len(footers) > 0:
                with z.open(footers[0]) as footer:
                    for k in args.keywords:
                        if k in footer.read().decode():
                            logging.warning("\"{}\" is a canary file!".format(f))
