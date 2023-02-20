import shutil 
import random
import os 
import argparse
from tqdm import tqdm


def sample_copy_save(config):
    
    source = config.source
    destination = config.destination
    
    # make destination directory
    try:
        os.makedirs(destination, exist_ok=True)
    except OSError as error:
        print("Directory '%s' can not be created" %destination)
    
    
    # read the files in source 
    files = os.listdir(source)
    
    sampled = random.sample(population=files, k=config.k)
    
    # move the file from source to 
    
    for each in tqdm(sampled):
        shutil.copy(os.path.join(source, each), os.path.join(destination, each))






def main():
    
    parser = argparse.ArgumentParser(description='Sample memes from one folder and copy it to another.')
    
    required_args = parser.add_argument_group('required arguments')
    
    required_args.add_argument('--source', type=str, dest='source', help="Which subreddit to scrap?", required=True)
    required_args.add_argument('--destination', type=str,dest='destination', help="Unix timestamp after which to scrap images?", required=True)
    required_args.add_argument('--k', type=int, dest='k', help="Unix timestamp before which to scrap images?", required=True)

    args = parser.parse_args()
    
    sample_copy_save(config=args)
    
    # print(len(data))


if __name__ == '__main__':
    main()