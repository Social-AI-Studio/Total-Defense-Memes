import shutil
import os
import easyocr
from PIL import Image
import json
import pandas as pd
import ast
from imagededup.methods import PHash
import numpy as np
from joblib import Parallel, delayed

# renames the collected files with scrape source(google,insta,reddit) and index
def copy_and_rename(files,dest,scrape_source='',start_indx=0):
    success=0
    errors=[]
    file_name_map={}
    for index,file in enumerate(files):
        extn=file.split("/")[-1].split(".")[-1]
        try:
            rename='{}_{}.{}'.format(scrape_source,index+start_indx,extn)
            file_name_map[rename]=file.split("/")[-1]
            shutil.copyfile(file,os.path.join(dest,rename))
            success+=1
        except OSError as e:    
            print("error copying file {} due to {}".format(file,e))
            errors.append(file)
    return success,errors,file_name_map

# renames visuals collected through google keyword search
def copy_map_and_rename(files,dest):
    success=0
    errors=[]
    not_found=[]
    file_name_map={}
    for index,file in enumerate(files):
        name=file.split("/")[-1].split("_")[0]
        extn=file.split("/")[-1].split(".")[-1]
        try:
            if name.lower() in [_.lower() for _ in 
                ["Singapore air force memes",
                "Singapore defense memes",
                "Singapore national service memes",
                "Singapore military memes",
                "memedef Singapore",
                "NSF Singapore memes",
                "Singapore air force memes site:reddit.com",
                "Singapore military memes site:instagram.com"
            ]]:
                rename='military_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["Singapore police force memes",
                "singapore police memes",
                "singapore civil memes", 
                "Singapore police memes site:reddit.com",
                "Singapore police memes site:instagram.com"
            ]]:
                rename='civil_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["singapore new water memes",
                "singapore economics memes",
                "singapore cpf memes",
                "Singapore HDB memes",
                "Singapore finance memes", 
                "Singapore fresh chicken export ban memes",
                "Singapore new water memes site:reddit.com",
                "Singapore finance meme site:reddit.com",
                "Singapore finance meme site:twitter.com"
            ]]:
                rename='economic_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["Singapore social memes",
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
            ]]:
                rename='social_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["singapore government memes",
                "singapore mental health memes",
                "Singapore government memes site:reddit.com",
                "Singapore government memes site:twitter.com"
            ]]:
                rename='psychological_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["singapore tech memes",
                "singapore scamming memes",
                "singapore misinformation memes",
                "singapore phishing memes",
                "singapore smart nation memes",
                "Singapore tech memes site:reddit.com",
                "Singapore scamming memes site:twitter.com"
            ]]:
                rename='digital_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            elif name.lower() in [_.lower() for _ in 
                ["Singapore COVID-19 mask memes [COVID-19]",
                "Singapore COVID-19 memes [COVID-19]",
                "Singapore tracetogether memes",
                "Singapore East Coast Memes",
                "Singapore Heng Swee Heng Memes",
                "Singapore NDP Memes",
                "Singapore memes site:reddit.com",
                "Singapore memes site:instagram.com",
                "Singapore memes site:twitter.com"
            ]]:
                rename='others_{}.{}'.format(index,extn)
                file_name_map[rename]=file.split("/")[-1]
                shutil.copyfile(file,os.path.join(dest,rename))
                success+=1
            else:
                not_found.append(file)
        except OSError as e:
            print("index:{}, {} not copied due to:{}".format(index,file,e))
            errors.append(file)
    return success,not_found,errors,file_name_map

def copy_file(file,dest):
    try:
        shutil.copy(file,dest)
        return 1
    except:
        return 0 

# file copy
def copy(files, dest):   
    success=0;errors=0
    temp= Parallel(n_jobs=20)(delayed(copy_file)(file,dest) for file in files)
    success,errors=sum(temp),len(temp)-sum(temp)
    # for index,file in enumerate(files):
    #     try:
    #         shutil.copy(file,dest)
    #         success+=1
    #     except OSError as e:    
            # print("error copying file {} due to {}".format(file,e))
            # errors.append(file)   
    return success,errors 

# same files are collected multiple times from google download, getting unique out of them
def get_unique_filenames(files):
    unique_file_names=[]
    seen=[]
    for file in files:  
        name=file.split("/")[-1]
        if(name in seen):
            continue
        else:
            seen.append(name)
        unique_file_names.append(file)
    return unique_file_names

# checks for corruption in downloaded files
def chk_file_corrupted(file,retained_exts):
    try:
        img = Image.open(file)  # open the image file
        img.verify()  # verify that it is, in fact an image

        exts=img.format

        if img.format in retained_exts:
            return file,img.size
    except (IOError, SyntaxError) as e:
        # print('Bad file:', filepath) # print out the names of corrupt files
        return

# filtes corrupted files
def return_non_corrupted_files(path):
    files = os.listdir(path)

    retained_files = []
    detected_exts, retained_exts = [], ['PNG','JPEG']
    # file_sizes={}
    filepaths=[os.path.join(path, file) for file in files]
    temp= Parallel(n_jobs=20)(delayed(chk_file_corrupted)(filepath,retained_exts) for filepath in filepaths)
    retained_files=[item for item in temp if item is not None]
    return retained_files
    # for filepath in files:
    #     _, ext = os.path.splitext(filepath)
    #     # if ext in ['.png', '.jpg']:
    #     try:
    #         img = Image.open(os.path.join(path, filepath)
    #                          )  # open the image file
    #         img.verify()  # verify that it is, in fact an image

    #         detected_exts.append(img.format)

    #         if img.format in retained_exts:
    #             retained_files.append(filepath)
    #             file_sizes[filepath]=img.size
    #     except (IOError, SyntaxError) as e:
    #         # print('Bad file:', filepath) # print out the names of corrupt files
    #         pass

    # detected_exts = set(detected_exts)

    # print(f"Detected Extensions: {detected_exts}")
    # print(f"Retained Extensions: {retained_exts}")
    # print(f"Num. Retained Files: {len(retained_files)}/{len(files)}")

    # return retained_files, file_sizes

# extracts text from visuals
def read_txt(files):
    reader = easyocr.Reader(['en'], gpu=True)
    ocr_text={}
    error_files=[]
    no_text_files=[]
    for index,file in enumerate(files):
        try:    
            text=reader.readtext(file)
        except:
            error_files.append(file)
            continue
        if(len(text)==0):   
            no_text_files.append(file)
        else:
            ocr_text[file.split("/")[-1]]=text
        print(index,end="\r")    
    return ocr_text,error_files,no_text_files 

# deduplicates using pHash
def return_duplicates(path,thresh=1):
    phasher = PHash()
    encodings = phasher.encode_images(image_dir=path)
    
    duplicates = phasher.find_duplicates(encoding_map=encodings,max_distance_threshold=thresh,scores=False)
    duplicates_to_remove = phasher.find_duplicates_to_remove(encoding_map=encodings)
    
    print("Num. Duplicates:", len(duplicates), type(duplicates))
    print("Num. Duplicates (Removal):", len(duplicates), type(duplicates_to_remove))

    return duplicates

# removing duplicates(from each set of duplicates, visual with biggest size is retrained)
def get_unique_samples(duplicates:dict,ocr_text:dict,file_sizes:dict):
    unique_samples=[]
    seen=[]
    counter=0
    for key,values in duplicates.items():
        if(key not in seen):
            temp=[]    
            temp.append(ocr_text[key]) 
            dups=[value for value in values if value not in seen and ocr_text[value]==ocr_text[key]]
            sizes=[file_sizes[key],*[file_sizes[dup] for dup in dups]]
            max_size_index=0
            for index in range(len(sizes)):
                if(sizes[index][0]>sizes[max_size_index][0] and sizes[index][1]>sizes[max_size_index][1]):
                    max_size_index=index
            if(max_size_index==0):
                unique_samples.append(key)
            else:
                unique_samples.append(dups[max_size_index-1]) 
            seen.extend(dups)       

        for value in values:
            if value not in seen and ocr_text[value] not in temp:
                unique_samples.append(value)
            temp.append(ocr_text[value])    
        seen.append(key)
        seen.extend(values)
        counter+=1
        print(counter,end="\r")    
    return unique_samples                       
