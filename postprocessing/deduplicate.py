import argparse
import os
import shutil

from imagededup.methods import PHash

def return_duplicates(path):
    phasher = PHash()
    encodings = phasher.encode_images(image_dir=path)
    
    duplicates = phasher.find_duplicates(encoding_map=encodings)
    duplicates_to_remove = phasher.find_duplicates_to_remove(encoding_map=encodings)
    
    print("Num. Duplicates:", len(duplicates), type(duplicates))
    print("Num. Duplicates (Removal):", len(duplicates), type(duplicates_to_remove))

    return duplicates


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove Similar Visuals')
    parser.add_argument('--pillar', type=str,
                        help='the soft-label total defence pillar')
    parser.add_argument('--source', type=str,
                        help='source (raw) directory')
    parser.add_argument('--dest', type=str,
                        help='destination (processed) directory')
    parser.add_argument('--viz', type=str,
                        help='deduplicate visualization directory')
    args = parser.parse_args()


    # clear the existing item inside folder
    for file in os.listdir(args.dest):
        path = os.path.join(args.dest, file)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

    # Get duplications
    duplicates = return_duplicates(args.source)

    # Remove duplicates but keep 1 copy
    all_files = os.listdir(args.source)
    remaining_files, flagged_files = [], set()
    for filename in all_files:
        
        if filename in flagged_files:
            continue

        if filename in duplicates:
            flagged_files = flagged_files.union(set(duplicates[filename]))

        source = os.path.join(args.source, filename)
        destination = os.path.join(args.dest, filename)
        shutil.copyfile(source, destination)

        remaining_files.append(filename)

    print(f"Num. Remaining Files: {len(remaining_files)}/{len(all_files)}")