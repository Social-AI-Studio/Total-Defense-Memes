import os
import shutil
import glob2
import argparse


parser = argparse.ArgumentParser(
    description='Grouping Google Search Results into (Soft-Labeled) Total Defence Pillars')
parser.add_argument('--pillar', type=str,
                    help='the soft-label total defence pillar')
parser.add_argument('--source', type=str,
                    help='source (raw) directory')
parser.add_argument('--dest', type=str,
                    help='destination (processed) directory')
parser.add_argument('--batch', type=str,
                    help='batch1, batch2, ...')

keys_military = ["Singapore military memes",
                 "memedef Singapore", "Singapore national service memes",
                 "Singapore military memes site:instagram.com",
                 "Singapore military memes", "Singapore defense memes",
                 "Singapore air force memes site:reddit.comSingapore military memes site:instagram.com",
                 "Singapore air force memes site:reddit.com",
                 "Singapore air force memes",
                 "NSF_Singapore_Memes"]

keys_civil = ["Singapore police memes site:reddit.com",
              "Singapore police memes site:instagram.com",
              "Singapore police force memes",
              "singapore police memes",
              "singapore civil memes"]

keys_social = ["Singapore social memes",
               "Singapore culture memes",
               "Singapore Immigration memes",
               "singapore funny memes",
               "singapore memes",
               "singapore covid memes",
               "singapore lockdown memes",
               "singapore pandemic memes",
               "singapore food memes",
               "Singapore racial memes",
               "Singapore racist memes",
               "Singapore religion memes",
               "Singapore religious memes",
               "Singapore chinese memes",
               "Singapore malay memes",
               "Singapore indian memes",
               "Singapore racial memes site:reddit.com",
               "Singapore racist memes site:reddit.com",
               "Singapore racist memes site:twitter.com"
               ]

keys_others = [
    "COVID-19_mask_memes",
    "COVID-19_memes",
    "Singapore tracetogether memes",
    "Singapore East Coast Memes",
    "Singapore Heng Swee Heng Memes",
    "Singapore NDP Memes",
    "Singapore memes site:reddit.com",
    "Singapore memes site:instagram.com",
    "Singapore memes site:twitter.com"
]

keys_psychological = [
    "singapore government memes",
    "singapore mental health memes",
    "Singapore government memes site:reddit.com",
    "Singapore government memes site:twitter.com"
]

keys_digital = [
    "singapore tech memes",
    "singapore scamming memes",
    "singapore misinformation memes",
    "Singapore phishing memes",
    "Singapore smart nation memes",
    "Singapore tech memes site:reddit.com",
    "Singapore scamming memes site:twitter.com"
]

keys_economic = [
    "singapore new water memes",
    "singapore economics memes",
    "singapore cpf memes",
    "Singapore HDB memes",
    "Singapore finance memes",
    "Singapore fresh chicken export ban memes",
    "Singapore new water memes site:reddit.com",
    "Singapore finance meme site:reddit.com",
    "Singapore finance meme site:twitter.com"
]

# Remove corrupted files
args = parser.parse_args()
base_dir = f"/mnt/sda/dataset/google_search_results/{args.batch}"
source_dir = os.path.join(base_dir, args.source)
dest_dir = os.path.join(base_dir, "postprocessing", args.dest)

# clear all the folders
for pillar in ['civil', 'economics', 'military', 'social', 'psychological', 'digital']:
    pillar_dir = os.path.join(dest_dir, pillar)
    for files in os.listdir(pillar_dir):
        path = os.path.join(pillar_dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

# transfer the files
for folder in glob2.glob(f"{source_dir}/*"):
    fname = folder.split('/')[-1]

    if fname in keys_military:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'military'))
    elif fname in keys_civil:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'civil'))
    elif fname in keys_economic:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'economics'))
    elif fname in keys_social:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'social'))
    elif fname in keys_psychological:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'psychological'))
    elif fname in keys_digital:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'digital'))
    elif fname in keys_others:
        for file in glob2.glob("{}/*".format(folder)):
            shutil.copy(file, os.path.join(dest_dir, 'others'))
    else:
        raise ValueError(f"Uncategorized Folder: {folder}")
