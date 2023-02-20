from __future__ import annotations
from functools import partial
import numpy as np
import pandas as pd
import json
import os
import argparse
import ast
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import string
from nltk.tokenize import word_tokenize

num_annotators_thresh = 2
batch_size=300

def read_response(batch_folder='/Users/nirmal/Downloads/batches',batches='all',separate=False):
    if(batches=='all'):
        files=os.listdir(batch_folder)
        files=[file for file in files if "response_batch" in file]
        batches=[file.split("_batch")[-1].split(".json")[0] for file in files]
    else:
        batches=batches.split(",")
    if(separate):
        response={}
        for batch in batches:
            with open(os.path.join(batch_folder,"response_batch{}.json".format(batch)),"r") as f:
                response[batch]=pd.DataFrame(json.load(f)['screenings'])
    else:                
        response=[]
        for batch in batches:
            with open(os.path.join(batch_folder,"response_batch{}.json".format(batch)),"r") as f:
                response.append(pd.DataFrame(json.load(f)['screenings']))        
        response=pd.concat(response)
        # response=response.astype({"pillars": str, "stance": str})
    return response

def get_sg_meme_breakdown(batch_folder='/Users/nirmal/Downloads/batches',soft_pillar_agreement=True):
    '''
    Gets a snapshot of SG memes from all batches
    '''

    # filter completed memes
    complete_matches=[]
    response=read_response(batch_folder)
    response=response[response['createdAt']!=response['updatedAt']]
    meme_counts=response.groupby('memeId')['memeId'].count()
    meme_completed=meme_counts[meme_counts>=num_annotators_thresh].index.tolist()
    # response[response['memeId'].isin(meme_completed)].sort_values(by=['memeId'], ascending=True)\
    #     .to_csv("/Users/nirmal/Downloads/completed_memes.csv",index=False)
    non_memes=[]
    non_sg_memes=[]
    sg_meme_Ids=[]
    pillar_match_Ids=[]
    stance_matches_Ids=[]
    memes=[]
    pillar_match_types={}
    meme_texts=[]
    # matched_pillar_breakdown={}
    stop_words = set(stopwords.words('english'))
    pillar_stance_types={'Military Defence':{'Supportive':0,'Against':0,'Neutral':0},\
                'Civil Defence':{'Supportive':0,'Against':0,'Neutral':0},'Economic Defence':{'Supportive':0,'Against':0,'Neutral':0},\
                'Social Defence':{'Supportive':0,'Against':0,'Neutral':0},'Psychological Defence':{'Supportive':0,'Against':0,'Neutral':0},\
                'Digital Defence':{'Supportive':0,'Against':0,'Neutral':0},'Others':{'Supportive':0,'Against':0,'Neutral':0}}
    # get SG memes
    for memeId in meme_completed:
        temp=response[response['memeId']==memeId]
        if len(temp[temp['contentType']!='Meme'])>=num_annotators_thresh:
            non_memes.append((memeId,temp[temp['contentType']!='Meme']['filename'].iloc[0]))
        if len(temp[temp['contentType']=='Meme'])>=num_annotators_thresh:
            memes.append((memeId,temp['filename'].iloc[0]))

        if len(temp[temp['contentType']=='Meme'])>=num_annotators_thresh and \
            len(temp[temp['relatedCountry']!='SG'])>=num_annotators_thresh:
            non_sg_memes.append((memeId,temp['filename'].iloc[0])) 

        if len(temp[temp['contentType']=='Meme'])>=num_annotators_thresh and \
            len(temp[temp['relatedCountry']=='SG'])>=num_annotators_thresh:
            sg_meme_Ids.append((memeId,temp['filename'].iloc[0]))
        annotators=list(temp['annotatorId'])
        if(3 in annotators):
            text=temp[temp['annotatorId']==3]['text'].iloc[0]
        elif(5 in annotators):
            text=temp[temp['annotatorId']==5]['text'].iloc[0]
        elif(7 in annotators):
            text=temp[temp['annotatorId']==7]['text'].iloc[0]
        else:
            print(annotators)    
        meme_texts.append((memeId,temp['filename'].iloc[0],text))
    # two_match=[]    
    # print('len memes:',len(memes))   
    for memeId,_ in sg_meme_Ids:       
        temp=response[response['memeId']==memeId] 
        temp=temp[temp['relatedCountry']=='SG']
        # if annotated by 3, atleast 2 must agree or if annotated by 2, both must agree 
        temp_pillars=[tuple(item) for item in list(temp['pillars'])]
        temp_str=temp.astype({"pillars": str, "stance": str})
        if not soft_pillar_agreement and ((len(temp_str)==3 and len(set(temp_pillars))<=2) or \
            (len(temp_str)==2 and len(set(temp_pillars))==1)):                
                pillar_counts=temp_str.groupby('pillars')['pillars'].count()
                matching_pillars=pillar_counts[pillar_counts>=num_annotators_thresh].index.tolist()
                pillar_match_Ids.append((memeId,ast.literal_eval(matching_pillars[0])))
                # get counts of each type of pillars
                if(matching_pillars[0] in pillar_match_types):
                    pillar_match_types[matching_pillars[0]]+=1
                else:
                    pillar_match_types[matching_pillars[0]]=1    
                if(matching_pillars[0]=='[]'):
                    print(memeId)
                temp_str=temp_str[temp_str['pillars']==matching_pillars[0]]
                temp_stance=[tuple(item) for item in list(temp_str['stance'])]
                if (len(temp_str)==3 and len(set(temp_stance))<=2) or (len(temp_str)==2 and len(set(temp_stance))==1):
                    stance_matches_Ids.append(memeId)
                    # get matching stance
                    stance_counts=temp_str.groupby('stance')['stance'].count()
                    try:
                        matching_stance=stance_counts[stance_counts>=num_annotators_thresh]
                        matching_stance_str=matching_stance.index.tolist()[0]
                        matching_stance=ast.literal_eval(matching_stance_str)
                        tags=[]
                        matching_rows=temp_str[temp_str['stance']==matching_stance_str]
                        for _ in range(len(matching_rows)):
                            tags.extend(matching_rows['tags'].iloc[_])
                        complete_matches.append({'filename':matching_rows['filename'].iloc[0],\
                            'contentType':matching_rows['contentType'].iloc[0],'relatedCountry':matching_rows['relatedCountry'].iloc[0],\
                                'pillars':ast.literal_eval(matching_rows['pillars'].iloc[0]),\
                                    'stance':ast.literal_eval(matching_rows['stance'].iloc[0]),\
                                        'tags':tags})
                    except IndexError as e:
                        print('Improper stance for meme :{}'.format(memeId))    
                        return
                    for index,pillar in enumerate(ast.literal_eval(matching_pillars[0])):
                        pillar_stance_types[pillar][matching_stance[index]]+=1
        # unordered complete matches
        # elif(len(temp)==3 and len(set([tuple(sorted(pillars)) for pillars in list(temp['pillars'])]))<=2) or\
        #     (len(temp)==2 and len(set([tuple(sorted(pillars)) for pillars in list(temp['pillars'])]))==1):
        #     pillar_list=list(temp['pillars'])
        #     sorted_pillars=[sorted(pillars) for pillars in pillar_list]
            
        #     pillar_match_indices=[_ for _,item in enumerate(sorted_pillars) if sorted_pillars.count(item)>1]
        #     matching_pillar=pillar_list[pillar_match_indices[0]]
        #     if(matching_pillar in pillar_match_types):
        #         pillar_match_types[matching_pillar]+=1
        #     else:
        #         pillar_match_types[matching_pillar]=1 
        #     pillar_match_Ids.append((memeId,ast.literal_eval(matching_pillar)))

        #     stances=list(temp['stance'])
        #     sorted_stances=[(stances[ind] for ind in np.argsort(pillar_list[index])) for index in pillar_match_indices]
        #     matching_stance=stances[[_ for _,item in enumerate(sorted_stances) if sorted_stances.count(item)>1][0]]
        #     if(len(pillar_match_indices)==3 and len(set(sorted_stances))<=2) or\
        #          (len(pillar_match_indices)==2 and len(set(sorted_stances))==1):
        #         stance_matches_Ids.append(memeId)
        #         for index,pillar in enumerate(ast.literal_eval(matching_pillars)):
        #             pillar_stance_types[pillar][matching_stance[index]]+=1
        #         tags=[]
        #         for index in pillar_match_indices:
        #             tags.extend(temp['tags'].iloc[index])    
        #         complete_matches.append({'filename':temp['filename'].iloc[0],\
        #             'contentType':temp['contentType'].iloc[0],'relatedCountry':matching_stance['relatedCountry'].iloc[0],\
        #                 'pillars':ast.literal_eval(matching_rows['pillars'].iloc[0]),\
        #                     'stance':ast.literal_eval(matching_rows['stance'].iloc[0]),\
        #                         'tags':tags})   
        #     print('unordered complete match ',memeId)        
        # patial matches                
        elif(soft_pillar_agreement):
            # check if any of the annotators have marked multiple pillars for the meme
            # if any([len(temp['pillars'].iloc[index])>1 for index in range(len(temp))]):
                # get all unique pillars marked by the annotators for the meme
            unique_pillars=set([pillar for pillars in list(temp['pillars']) for pillar in pillars])
            matched_pillars=[]
            # ============get more than 1 pillar soft matches==========
            # test=[]
            # for pillar in unique_pillars:
            #     # for a pillar if at least 2 annotators include it, this is considered a match
            #     if(sum([pillar in row['pillars'] for _,row in temp.iterrows()])>=2):
            #         # pillar_match_Ids.append(memeId)
            #         test.append(pillar)
            # if(len(test)>1):
            #     two_match.append(memeId)
            # ==========================================================

            for pillar in unique_pillars:
                # for a pillar if at least 2 annotators include it, this is considered a match
                if(sum([pillar in row['pillars'] for _,row in temp.iterrows()])>=2):
                    # pillar_match_Ids.append(memeId)
                    matched_pillars.append(pillar)
            if(len(matched_pillars)>0):       
                pillar_match_Ids.append((memeId,matched_pillars))        
            # update the matched pillar type 
            for matched_pillar in matched_pillars:   
                if(matched_pillar in pillar_match_types):
                    pillar_match_types[matched_pillar]+=1
                else:
                    pillar_match_types[matched_pillar]=1  
            # filter the rows where match pillar exists 
            tags=[]
            # if(len(matched_pillars) in matched_pillar_breakdown):
            #     matched_pillar_breakdown[len(matched_pillars)]+=1
            # else:
            #     matched_pillar_breakdown[len(matched_pillars)]=1                     
            stances=[]
            pillar_match_stances=[]
            for matched_pillar in matched_pillars:            
                temp_match=pd.DataFrame([row for _,row in temp.iterrows() if matched_pillar in row['pillars']]) 
                for _,row in temp_match.iterrows():
                    row_tags=[token.strip() for token in row['tags'] if token.lower() not in stop_words]
                    # row_tags=tags=[t.strip() for tag in row_tags for t in tag]
                    row_tags=[tg for tg in row_tags if " {} ".format(tg.lower()) not in " ".join(row_tags)]
                    row_tags=[tg for tg in row_tags if all([tg.replace(punc,"").lower() not in stop_words for punc in string.punctuation])]    
                    
                    row_tags=[t.strip() for tag in row_tags for t in tag.split(",") if t.lower() not in stop_words and t!='' \
                        and all([token.lower() not in tg.lower() for tg in tags for token in t.split(" ")])]  
                        
                    tags.extend(list(set(row_tags)))
                matched_stances=[]
                
                for _,row in temp_match.iterrows():
                    pillars=row['pillars']
                    if matched_pillar in pillars:
                        matched_stances.append(row['stance'][pillars.index(matched_pillar)])
                pillar_match_stances.append((matched_pillar,matched_stances))

                if (len(temp_match)==3 and len(set(matched_stances))<=2) or (len(temp_match)==2 and len(set(matched_stances))==1):
                    if(memeId not in stance_matches_Ids):
                        stance_matches_Ids.append(memeId) 
                    matched_stance=[stance for stance in matched_stances if matched_stances.count(stance)>1][0] 
                    # for _,row in temp.iterrows():
                    #     if(matched_pillar in row['pillars'] and matched_stance in row['stance']):
                    #         tags.extend(row['tags'])
                    pillar_stance_types[pillar][matched_stance]+=1
                    stances.append((matched_pillar,matched_stance))
                    # stances.append(matched_stance)
                else:
                    # stances.append('not matched') 
                    continue   
            tags=list(set(tags))
            
            if(len(tags)>0):
                # common_tags=set(tags[0]) 
                # for tag in tags:
                #     common_tags=common_tags.intersection(set(tag))
                # common_tags=list(common_tags) 
                # if(len(common_tags)==0):
                #     tags=tags[0]
                # else:
                #     tags=common_tags          
                complete_matches.append({'memeId':memeId,'filename':temp['filename'].iloc[0],'pillar_match_stances':pillar_match_stances,\
                'contentType':temp['contentType'].iloc[0],'relatedCountry':temp['relatedCountry'].iloc[0],\
                    'pillars':matched_pillars,'stance':stances,'tags':tags})                                
            # print('soft match ',memeId)        
    # print(matched_pillar_breakdown)
    sg_memes= {'non_memes':non_memes,'memes':memes,'non_sg_memes':non_sg_memes,'sg_memes':sg_meme_Ids,\
                    'meme_texts':meme_texts,'pillar_matches':pillar_match_Ids,\
                    'stance_matches':stance_matches_Ids,'pillar_match_types':len(pillar_match_types),'matched_memes':complete_matches}   
    with open(os.path.join(batch_folder,"sg_memes.json"),"w") as f:
        json.dump(sg_memes,f)    
    return {'non_memes':len(non_memes),'memes':len(memes),'non_sg_memes':len(non_sg_memes),'sg_memes':len(sg_meme_Ids),\
        'pillar_matches':len(pillar_match_Ids),'stance_matches':len(stance_matches_Ids),\
        'pillar_match_types':pillar_match_types,'pillar_stance_types':pillar_stance_types}        


def get_conflicts(ann_ids=[3,4,5,6,7,8,9],batch_folder='/Users/nirmal/Downloads/batches',batches='all',soft_pillar_agreement=True):
    '''
    Returns detailed count of conflicts between annotators and given batches
    Also, saves the meme ids of each type of conflict
    '''

    # filter with annotaor ids and completed memes
    response=read_response(batch_folder,batches)
    response=response[response['annotatorId'].isin(ann_ids)]
    total_meme_count=len(set(list(response['memeId'])))
    response=response[response['createdAt']!=response['updatedAt']]
    meme_counts=response.groupby('memeId')['memeId'].count()
    meme_completed=meme_counts[meme_counts>=num_annotators_thresh].index.tolist()
    print('{} meme completed out of {}'.format(len(meme_completed),total_meme_count))

    contentType_conflicts=[]
    relatedCountry_conflicts=[]
    pillars_conflicts=[]
    stance_conflicts=[]
    text_conflicts=[]
    for memeId in meme_completed:
        temp=response[response['memeId']==memeId]
        temp_str=temp.astype({"pillars": str, "stance": str})
        # if a meme has been annotated by 3 annotators, 2 must agree
        if(len(temp)==3):
            unique_thresh=2
        # if a meme has been annotated by 2 annotators, both must agree
        elif(len(temp)==2):
            unique_thresh=1
        texts=[item.lower().replace("\n"," ").strip() for item in list(temp['text'])]
        texts=[" ".join([t for t in text.split(" ") if t!='']) for text in texts]
        texts_filtered=[]
        for text in texts:
            temp_toks=[]
            for token in word_tokenize(text):
                for punc in string.punctuation:
                    token=token.replace(punc,"")
                if(token!=""):    
                    temp_toks.append(token)
            texts_filtered.append(" ".join(temp_toks).strip())        
        # texts=[" ".join([token for token in word_tokenize(text) for punc in string.punctuation]) for text in texts]
        if(len(set(texts_filtered))>unique_thresh):
            # text_conflicts.append(memeId)    
            if(len(texts_filtered)==3):
                texts_filtered=texts_filtered[:2]
            conflicting_texts=[token for token in texts_filtered[0].split(" ") if token not in texts_filtered[1].split(" ")]
            conflicting_texts.extend([token for token in texts_filtered[1].split(" ") if token not in texts_filtered[0].split(" ")])
            text_conflicts.append((memeId,temp['filename'].iloc[0],conflicting_texts)) 
        if(len(set(list(temp['contentType'])))>unique_thresh):
            contentType_conflicts.append(memeId)
        elif(len(set(list(temp['contentType'])))<=unique_thresh \
            and len(set(list(temp['relatedCountry'])))>unique_thresh):
            relatedCountry_conflicts.append(memeId) 
        elif len(temp[temp['contentType']=='Meme'])>=num_annotators_thresh and \
            len(temp[temp['relatedCountry']=='SG'])>=num_annotators_thresh:
            temp=temp[temp['relatedCountry']=='SG']
            temp_str=temp_str[temp_str['relatedCountry']=='SG']
            # check if any of the annotators have marked multiple pillars for the meme
            if not soft_pillar_agreement or all([len(temp['pillars'].iloc[index])==1 for index in range(len(temp))]):
                if(len(temp)==3 and len(list(set(temp_str['pillars'])))>2):
                    pillars_conflicts.append(memeId)
                elif(len(temp)==2 and len(list(set(temp_str['pillars'])))>1):
                    pillars_conflicts.append(memeId)    
                else:
                    # get the pillar where match occurs
                    pillar_counts=temp_str.groupby('pillars')['pillars'].count()
                    matching_pillars=pillar_counts[pillar_counts>=num_annotators_thresh].index.tolist()
                    if(matching_pillars[0]=='[]'):
                        print(memeId)
                    temp=temp_str[temp_str['pillars']==matching_pillars[0]]
                    # get stance match for matching pillars
                    if (len(temp)==3 and len(set(list(temp['stance'])))>2) or (len(temp)==2 and len(set(list(temp['stance'])))>1):
                        stance_conflicts.append(memeId)
            else:
                unique_pillars=set([pillar for pillars in list(temp['pillars']) for pillar in pillars])
                matched_pillars=[]
                for pillar in unique_pillars:
                    # for a pillar if at least 2 annotators include it, this is considered a match
                    if(sum([pillar in row['pillars'] for _,row in temp.iterrows()])>=2):
                        # pillar_match_Ids.append(memeId)
                        matched_pillars.append(pillar)
                # update the matched pillar type    
                if(len(matched_pillars)==0):
                    pillars_conflicts.append(memeId)
                else:
                    stance_conflict=True
                    for matched_pillar in matched_pillars:
                        temp2=pd.DataFrame([row for _,row in temp.iterrows() if matched_pillar in row['pillars']]) 
                        matched_stances=[]
                        for _,row in temp2.iterrows():
                            pillars=row['pillars']
                            if matched_pillar in pillars:
                                matched_stances.append(row['stance'][pillars.index(matched_pillar)])
                        # if(memeId==303):
                        #     print(matched_pillar,matched_stances)        
                        if (len(temp2)==3 and len(set(matched_stances))<=2) or (len(temp2)==2 and len(set(matched_stances))==1):
                            stance_conflict=False
                            break
                    if(stance_conflict):
                        stance_conflicts.append(memeId)


    conflicts= {'textConflicts':text_conflicts,'contentTypeConflicts':contentType_conflicts,'relatedCountryConflicts':relatedCountry_conflicts,\
        'pillarConflicts':pillars_conflicts,'stanceConflicts':stance_conflicts}
    batches="_".join(batches.split(",")) if batches!='all' else batches   
    with open(os.path.join(batch_folder,"annID_{}_batches_{}_conflicts.json".format("_".join([str(id) for id in ann_ids]),batches)),"w") as f:
        json.dump(conflicts,f)    
    return {'contentTypeConflicts':len(contentType_conflicts),'relatedCountryConflicts':len(relatedCountry_conflicts),\
        'pillarConflicts':len(pillars_conflicts),'stanceConflicts':len(stance_conflicts),'textConflicts':len(text_conflicts)}    

def get_matched_stance(matched_pillars,df):
    matched_pillar_stance=[]
    for matched_pillar in matched_pillars:            
        temp_match=pd.DataFrame([row for _,row in df.iterrows() if matched_pillar in row['pillars']]) 
        matched_stances=[]
        for _,row in temp_match.iterrows():
            pillars=row['pillars']
            if matched_pillar in pillars:
                matched_stances.append(row['stance'][pillars.index(matched_pillar)])
        if (len(temp_match)==3 and len(set(matched_stances))<=2) or (len(temp_match)==2 and len(set(matched_stances))==1):
            matched_stance=[stance for stance in matched_stances if matched_stances.count(stance)>1][0] 
            matched_pillar_stance.append((matched_pillar,matched_stance)) 
    return matched_pillar_stance        

def get_pair_agreements(ann_ids=[3,4],batch_folder='/Users/nirmal/Downloads/batches'):
    '''
    Returns a count of complete agreement between a pair of annotators
    '''

    # read all batches and filter for annotator ids and completed memes
    response=read_response(batch_folder)
    response=response[response['annotatorId'].isin(ann_ids)]
    response=response[response['createdAt']!=response['updatedAt']]
    meme_counts=response.groupby('memeId')['memeId'].count()
    meme_completed=meme_counts[meme_counts>=num_annotators_thresh].index.tolist()
    
    # get meme count which have complete agreement
    match_count=0
    for memeId in meme_completed:
        temp=response[response['memeId']==memeId]
        if (temp['contentType'].iat[0]==temp['contentType'].iat[1]) and \
            (temp['relatedCountry'].iat[0]==temp['relatedCountry'].iat[1]) and \
                (temp['pillars'].iat[0]==temp['pillars'].iat[1]) and \
                    (temp['stance'].iat[0]==temp['stance'].iat[1]):
                        match_count+=1

    # get cohen's kappa for all batches
    response=read_response(batch_folder,separate=True)
    filtered=[]
    for batch,df in response.items():
        # if(batch in ['1','3','5','7','9','11']):
        #     filtered.append(df[df['annotatorId'].isin([3,4])])
        # elif(batch in ['2','4','6']):
        #     filtered.append(df[df['annotatorId'].isin([6,7])])    
        # else:
        filtered.append(df)
    df=pd.concat(filtered)         
    scores={}
    df=df[df['createdAt']!=df['updatedAt']]
    meme_counts=df.groupby('memeId')['memeId'].count()
    meme_completed=meme_counts[meme_counts>=num_annotators_thresh].index.tolist()
    print("kappa calculated on {} visuals".format(len(meme_completed)))

    with open(os.path.join(batch_folder,"sg_memes.json"),"r") as f:
        match_data=json.load(f)
    matched_non_memes=[item[0] for item in match_data['non_memes']]    
    matched_sg_memes=[item[0] for item in match_data['sg_memes']] 
    matched_non_sg_memes=[item[0] for item in match_data['non_sg_memes']]
    matched_memes=matched_sg_memes+matched_non_sg_memes
    matched_pillars=match_data['matched_memes']
    matched_pillars={item['filename']:item['pillars'] for item in matched_pillars}
    stance_match_ids=match_data['stance_matches']
    print("len matched pillars",len(matched_pillars))
    ann1=[]
    ann2=[]
    for memeId in meme_completed:
        temp=df[df['memeId']==memeId]
        if(len(temp)==2):
            ann1.append(temp['contentType'].iloc[0])
            ann2.append(temp['contentType'].iloc[1]) 
        elif memeId in matched_non_memes:
            ann1.append('Non-Meme')
            ann2.append('Non-Meme')
        elif memeId in matched_memes:
            ann1.append('Meme')
            ann2.append('Meme')    
    scores['contentType']=cohen_kappa([item if item!='' else 'Non-Meme' for item in ann1],\
        [item if item!='' else 'Non-Meme' for item in ann2])

    ann1=[]
    ann2=[]
    for memeId in meme_completed:
        temp=df[df['memeId']==memeId]
        if(len(temp)==2):
            ann1.append(temp['relatedCountry'].iloc[0])
            ann2.append(temp['relatedCountry'].iloc[1]) 
        elif memeId in matched_sg_memes:
            ann1.append('SG')
            ann2.append('SG')
        elif memeId in matched_non_sg_memes:
            ann1.append('Non-SG')
            ann2.append('Non-SG')    
    scores['relatedCountry']=cohen_kappa([item if item!='' else 'Non-SG' for item in ann1],\
        [item if item!='' else 'Non-SG' for item in ann2])    

    # ann1=pd.DataFrame(ann1)
    # ann2=pd.DataFrame(ann2)    
    # ann1=ann1.sort_values(by=['memeId'], ascending=True)
    # ann2=ann2.sort_values(by=['memeId'], ascending=True)
    
    # scores['contentType']=cohen_kappa([item if item!='' else 'Non-Meme' for item in list(ann1['contentType'])],\
    #     [item if item!='' else 'Non-Meme' for item in list(ann2['contentType'])])
    # scores['relatedCountry']=cohen_kappa([item if item!='' else 'Non-SG' for item in list(ann1['relatedCountry'])],\
    #     [item if item!='' else 'Non-SG' for item in list(ann2['relatedCountry'])])

    meme_sg_ids=[]
    stance_match_files=[]
    for memeId in matched_sg_memes:
        temp=df[df['memeId']==memeId]
        # if (temp['contentType'].iloc[0]==temp['contentType'].iloc[1]=='Meme') and \
        #     (temp['relatedCountry'].iloc[0]==temp['relatedCountry'].iloc[1]=='SG'):
        meme_sg_ids.append(temp['filename'].iloc[0])
        if(memeId in stance_match_ids):
            stance_match_files.append(temp['filename'].iloc[0])
    print("len stance match files:",len(stance_match_files))
    ann1=[]
    ann2=[] 
    ann1_matched_pillars=[]
    ann2_matched_pillars=[]
    an1_stances=[]
    an2_stances=[]
    # count=0   
    # stance_matches=[]    
    for filename in meme_sg_ids:
        temp=df[df['filename']==filename]
        # if(filename in stance_match_files):
        #     stance_matches.append(temp)
        #     count+=1
        if(len(temp)==2):
            ann1.append(temp['pillars'].iloc[0])
            ann2.append(temp['pillars'].iloc[1])
            if(filename in matched_pillars):
                ann1_matched_pillars.append(temp['pillars'].iloc[0])
                ann2_matched_pillars.append(temp['pillars'].iloc[1])
                an1_stances.append(temp['stance'].iloc[0])
                an2_stances.append(temp['stance'].iloc[1])
        elif filename in matched_pillars:
            matching_pillars=matched_pillars[filename]
            matching_pillar_stance=get_matched_stance(matching_pillars,temp)
            pillar=matching_pillars[0]  
            if(len(matching_pillar_stance)==0): 
                if pillar in temp['pillars'].iloc[0]:
                    ann1.append(temp['pillars'].iloc[0])
                    an1_stances.append(temp['stance'].iloc[0])
                    ann1_matched_pillars.append(temp['pillars'].iloc[0])
                    if pillar in temp['pillars'].iloc[1]:
                        ann2.append(temp['pillars'].iloc[1])
                        ann2_matched_pillars.append(temp['pillars'].iloc[1])
                        an2_stances.append(temp['stance'].iloc[1])
                    else:
                        ann2.append(temp['pillars'].iloc[2])
                        ann2_matched_pillars.append(temp['pillars'].iloc[2])
                        an2_stances.append(temp['stance'].iloc[2])    
                elif pillar in temp['pillars'].iloc[1]:
                    ann1.append(temp['pillars'].iloc[1])
                    ann2.append(temp['pillars'].iloc[2]) 
                    ann1_matched_pillars.append(temp['pillars'].iloc[1])
                    ann2_matched_pillars.append(temp['pillars'].iloc[2])
                    an1_stances.append(temp['stance'].iloc[1])
                    an2_stances.append(temp['stance'].iloc[2])
            else:      
                pillar= matching_pillar_stance[0][0]
                if pillar in temp['pillars'].iloc[0] and pillar in temp['pillars'].iloc[1] \
                    and list(temp['stance'].iloc[0])[temp['pillars'].iloc[0].index(pillar)]\
                    ==list(temp['stance'].iloc[1])[temp['pillars'].iloc[1].index(pillar)]:
                        ann1.append(temp['pillars'].iloc[0])
                        an1_stances.append(temp['stance'].iloc[0])
                        ann1_matched_pillars.append(temp['pillars'].iloc[0])                    
                        ann2.append(temp['pillars'].iloc[1])
                        ann2_matched_pillars.append(temp['pillars'].iloc[1])
                        an2_stances.append(temp['stance'].iloc[1])
                elif pillar in temp['pillars'].iloc[0] and pillar in temp['pillars'].iloc[2] \
                    and list(temp['stance'].iloc[0])[temp['pillars'].iloc[0].index(pillar)]\
                    ==list(temp['stance'].iloc[2])[temp['pillars'].iloc[2].index(pillar)]:
                        ann1.append(temp['pillars'].iloc[0])
                        an1_stances.append(temp['stance'].iloc[0])
                        ann1_matched_pillars.append(temp['pillars'].iloc[0])                    
                        ann2.append(temp['pillars'].iloc[2])
                        ann2_matched_pillars.append(temp['pillars'].iloc[2])
                        an2_stances.append(temp['stance'].iloc[2])    
                elif pillar in temp['pillars'].iloc[1] and pillar in temp['pillars'].iloc[2] \
                    and list(temp['stance'].iloc[1])[temp['pillars'].iloc[1].index(pillar)]\
                    ==list(temp['stance'].iloc[2])[temp['pillars'].iloc[2].index(pillar)]:
                        ann1.append(temp['pillars'].iloc[1])
                        an1_stances.append(temp['stance'].iloc[1])
                        ann1_matched_pillars.append(temp['pillars'].iloc[1])                    
                        ann2.append(temp['pillars'].iloc[2])
                        ann2_matched_pillars.append(temp['pillars'].iloc[2])
                        an2_stances.append(temp['stance'].iloc[2])  
        else:
            ann1.append(temp['pillars'].iloc[0])
            ann2.append(temp['pillars'].iloc[1])    
                      

        # ann1=ann1[ann1['memeId'].isin(meme_sg_ids)].sort_values(by=['memeId'], ascending=True)
        # ann2=ann2[ann2['memeId'].isin(meme_sg_ids)].sort_values(by=['memeId'], ascending=True)
    # print("stance match count",count)
    # stance_matches=pd.concat(stance_matches)
    # stance_matches.to_csv("/Users/nirmal/Downloads/stance_matches.csv")
    scores['pillars']=cohen_kappa([tuple(item) for item in ann1],[tuple(item) for item in ann2],\
                partial_match=True)
    # an1_stances=[tuple(item) for item in list(ann1['stance'])]
    # an2_stances=[tuple(item) for item in list(ann2['stance'])]
    an1_stances_filtered=[]
    an2_stances_filtered=[]
    count=0
    for index,(pillar1,pillar2) in enumerate(zip([tuple(item) for item in ann1_matched_pillars],\
        [tuple(item) for item in ann2_matched_pillars])):
        # if any([item in pillar1 for item in pillar2 if item!='']):
        #     pillar_match_indices.append(index)
        
        added=False    
        for item in pillar2:
            if item!='' and item in pillar1:
                if not added and (an1_stances[index][pillar1.index(item)]==an2_stances[index][pillar2.index(item)]):
                    an1_stances_filtered.append(an1_stances[index][pillar1.index(item)])
                    an2_stances_filtered.append(an2_stances[index][pillar2.index(item)])
                    added=True 
        if not added:
            for item in pillar2:
                if item!='' and item in pillar1:
                    an1_stances_filtered.append(an1_stances[index][pillar1.index(item)])
                    an2_stances_filtered.append(an2_stances[index][pillar2.index(item)])
                    # print(an1_stances[index][pillar1.index(item)],an2_stances[index][pillar2.index(item)])   
                    break
    print(len(ann1),len(ann1_matched_pillars),len(an1_stances),len(an1_stances_filtered),count)
    scores['stance']=cohen_kappa(an1_stances_filtered,an2_stances_filtered)
    kappa_all_annotations=scores

    # get batch-wise cohen's kappa for each annotator pair
    kappa={}
    response=read_response(batch_folder,separate=True)
    for batch,df in response.items():
        if batch not in kappa:
            kappa[batch]={}
        unique_annotators=list(set(df['annotatorId']))
        unique_pairs=[list(zip([annId for _ in unique_annotators],unique_annotators)) for annId in unique_annotators]
        unique_pairs=list(set([tuple(sorted(pair)) for pairs in unique_pairs for pair in pairs if pair[0]!=pair[1]]))
        for pair in unique_pairs:
            # if(batch=='1' and pair==(3,4)):
            #     print(pair)
            scores={}
            temp=df[df['annotatorId'].isin(pair)]            
            temp=temp[temp['createdAt']!=temp['updatedAt']]
            meme_counts=temp.groupby('memeId')['memeId'].count()
            meme_completed=meme_counts[meme_counts>=num_annotators_thresh].index.tolist()
            if(len(meme_completed)==0):
                continue
            ann1=temp[(temp['annotatorId']==pair[0]) & (temp['memeId'].isin(meme_completed))].sort_values(by=['memeId'], ascending=True)
            ann2=temp[(temp['annotatorId']==pair[1]) & (temp['memeId'].isin(meme_completed))].sort_values(by=['memeId'], ascending=True)
            
            scores['contentType']=cohen_kappa([item if item!='' else 'Non-Meme' for item in list(ann1['contentType'])],\
                [item if item!='' else 'Non-Meme' for item in list(ann2['contentType'])])
            scores['relatedCountry']=cohen_kappa([item if item!='' else 'Non-SG' for item in list(ann1['relatedCountry'])],\
                [item if item!='' else 'Non-SG' for item in list(ann2['relatedCountry'])])
            
            meme_sg_ids=[]
            for memeId in meme_completed:
                temp_meme=temp[(temp['memeId']==memeId) & (temp['annotatorId'].isin(pair))]
                if (temp_meme['contentType'].iloc[0]==temp_meme['contentType'].iloc[1]=='Meme') and \
                    (temp_meme['relatedCountry'].iloc[0]==temp_meme['relatedCountry'].iloc[1]=='SG'):
                    meme_sg_ids.append(memeId)
            ann1=ann1[ann1['memeId'].isin(meme_sg_ids)].sort_values(by=['memeId'], ascending=True)
            ann2=ann2[ann2['memeId'].isin(meme_sg_ids)].sort_values(by=['memeId'], ascending=True)

            scores['pillars']=cohen_kappa([tuple(item) for item in list(ann1['pillars'])],[tuple(item) for item in list(ann2['pillars'])],\
                partial_match=True)
            an1_stances=[tuple(item) for item in list(ann1['stance'])]
            an2_stances=[tuple(item) for item in list(ann2['stance'])]
            an1_stances_filtered=[]
            an2_stances_filtered=[]
            for index,(pillar1,pillar2) in enumerate(zip([tuple(item) \
                for item in list(ann1['pillars'])],[tuple(item) for item in list(ann2['pillars'])])):
                # if any([item in pillar1 for item in pillar2 if item!='']):
                #     pillar_match_indices.append(index)
                for item in pillar2:
                    if item!='' and item in pillar1:
                        an1_stances_filtered.append(an1_stances[index][pillar1.index(item)])
                        an2_stances_filtered.append(an2_stances[index][pillar2.index(item)])

            scores['stance']=cohen_kappa(an1_stances_filtered,an2_stances_filtered)  
            # if(pair==(3,4) and batch=='1'):
            #     print(kappa,scores)      
            kappa[batch].update({pair:scores})
    return kappa_all_annotations,kappa,match_count,len(meme_completed)

def get_batch_annotator_progress(ann_ids=[3,4,5,6,7,8],batch_folder='/Users/nirmal/Downloads/batches'):
    completed={id:{} for id in ann_ids}
    response=read_response(batch_folder,separate=True)
    for batch,annotations in response.items():
        for ann_id,_ in completed.items():
            temp=annotations[annotations['annotatorId']==ann_id]
            if len(temp)>0:
                completed[ann_id].update({batch:len(temp[temp['createdAt']!=temp['updatedAt']])})
    return completed

def cohen_kappa(ann1, ann2,partial_match=False):
    """Computes Cohen kappa for pair-wise annotators.
    :param ann1: annotations provided by first annotator
    :type ann1: list
    :param ann2: annotations provided by second annotator
    :type ann2: list
    :rtype: float
    :return: Cohen kappa statistic
    """
    count = 0
    for an1, an2 in zip(ann1, ann2):
        if (not partial_match and an1 == an2):
            count += 1
        elif partial_match and any([item in an2 for item in an1 if item!='']):
            count += 1

    A = count / len(ann1)  # observed agreement A (Po)
    if(partial_match):
        ann1=[item for items in ann1 for item in items]
        ann2=[item for items in ann2 for item in items]

    uniq = set(ann1 + ann2)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = ((cnt1 / len(ann1)) * (cnt2 / len(ann2)))
        E += count

    return round((A - E) / (1 - E), 4)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-task', help='report to generate',choices=['get_conflicts','get_sg_meme_breakdown','get_pair_agreements',\
        'get_batch_annotator_progress'],\
        required=True,default='get_conflicts',type=str)
    parser.add_argument('-annIds', help='annotator Ids',required=False,default=[3,4,5,6,7,8,9],type=str)
    parser.add_argument('-batches', help='batches to consider',required=False,default='all',type=str)
    parser.add_argument('-batch_path', help='path of directory of batch json files',\
        required=False,default="/Users/nirmal/Downloads/batches",type=str)
    args = parser.parse_args()
    annIds=args.annIds
    if(type(args.annIds) is str):
        annIds=[int(id) for id in args.annIds.split(",")]
    if(args.task=='get_conflicts'):
        print(get_conflicts(annIds,args.batch_path,args.batches))
    elif(args.task=='get_sg_meme_breakdown'):    
        print(get_sg_meme_breakdown(args.batch_path))
    elif(args.task=='get_pair_agreements'):    
        kappa_all_annotations,kappa,match_count,meme_completed=get_pair_agreements(annIds,args.batch_path)
        print("kappa",kappa_all_annotations) 
        print("{} matches out of {} visuals".format(match_count,meme_completed))
    elif(args.task=='get_batch_annotator_progress'):
        print(get_batch_annotator_progress(annIds,args.batch_path))    
    
