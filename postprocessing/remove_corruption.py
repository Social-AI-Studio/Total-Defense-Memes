import argparse
import os
import shutil

from os import listdir
from PIL import Image


def return_non_corrupted_files(path):
    files = listdir(path)

    retained_files = []
    detected_exts, retained_exts = [], ['PNG', 'WEBP', 'JPEG']

    for filepath in files:
        _, ext = os.path.splitext(filepath)
        # if ext in ['.png', '.jpg']:
        try:
            img = Image.open(os.path.join(path, filepath)
                             )  # open the image file
            img.verify()  # verify that it is, in fact an image

            detected_exts.append(img.format)

            if img.format in retained_exts:
                retained_files.append(filepath)
        except (IOError, SyntaxError) as e:
            # print('Bad file:', filepath) # print out the names of corrupt files
            pass

    detected_exts = set(detected_exts)

    print(f"Detected Extensions: {detected_exts}")
    print(f"Retained Extensions: {retained_exts}")
    print(f"Num. Retained Files: {len(retained_files)}/{len(files)}")

    return retained_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Remove Corrupted Image and Non-Image Files')
    parser.add_argument('--pillar', type=str,
                        help='the soft-label total defence pillar')
    parser.add_argument('--source', type=str,
                        help='source (raw) directory')
    parser.add_argument('--dest', type=str,
                        help='destination (processed) directory')
    parser.add_argument('--batch', type=str,
                        help='batch1, batch2, ...')

    args = parser.parse_args()

    # clear the existing item inside folder
    for files in os.listdir(args.dest):
        path = os.path.join(args.dest, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

    # Remove corrupted files
    print(f"Processing {args.pillar.title()} Visuals")
    files = return_non_corrupted_files(args.source)

    # Save visuals (new names)
    files.sort()
    for index, filepath in enumerate(files):
        _, ext = os.path.splitext(filepath)
        new_filepath = f"{args.pillar}_{index}{ext}"

        source = os.path.join(args.source, filepath)
        destination = os.path.join(args.dest, new_filepath)

        shutil.copyfile(source, destination)
