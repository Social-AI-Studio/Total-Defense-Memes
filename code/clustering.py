from transformers import BertTokenizer, VisualBertModel
import re
import json
import torch
import pickle as pkl
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics import silhouette_score
from torchvision.models import vgg16
import torch.nn as nn
import PIL
from torchvision import transforms
import numpy as np
from transformers import BertTokenizer, BertModel
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from torchvision import transforms
import os

device=torch.device('cuda:1')


with open("./report/annotation.json","r") as f:
    annotation=json.load(f)
pillars=[file for item in annotation["Pillar_Stances"] for file,_ in item.items() if len(_)==1]

unique_pillars=[v for item in annotation["Pillar_Stances"] for k,v in item.items() if len(v)==1]
unique_pillars=[item[0][0] for item in unique_pillars ]
unique_pillars=list(set(unique_pillars))
unique_pillars={item:i for i,item in enumerate(unique_pillars)}
labels={k:unique_pillars[v[0][0]] for item in annotation["Pillar_Stances"] for k,v in item.items() if len(v)==1}

def run_kmeans(embedding="vlbert"):
    x=[]
    pillars=[file for item in annotation["Pillar_Stances"] for file,_ in item.items() if len(_)==1]
    if(embedding=="vlbert"):
        for file in pillars:
            with open("./vl_bert_embeddings/{}.pkl".\
                    format(file),"rb") as f:
                x.append(pkl.load(f))
    elif(embedding=="clip"):
        for file in pillars:
            with open("./clip_embeddings/{}.pkl".\
                    format(file),"rb") as f:
                temp=pkl.load(f)
                x.append(torch.cat((temp['text_embeds'],temp['image_embeds']),-1))
    elif(embedding=="bert"):
        for file in pillars:
            with open("./bert_embeddings/{}.pkl".\
                    format(file),"rb") as f:
                x.append(pkl.load(f))
    elif(embedding=="vgg"):
        for file in pillars:
            with open("./vgg_embeddings/{}.pkl".\
                    format(file),"rb") as f:
                x.append(pkl.load(f))
    x=torch.stack(x)  
    kmeans = KMeans(n_clusters=7, random_state=0, n_init=10).fit(x.squeeze(1).cpu().detach().numpy())
    kmeans_labels={file:kmeans.labels_[i] for i,file in enumerate(pillars)}
    nmi=normalized_mutual_info_score([lbl for file,lbl in labels.items()],[kmeans_labels[file] for file,lbl in labels.items()])
    ss=silhouette_score(np.array(x.squeeze(1).cpu().tolist()),kmeans.labels_)
    return nmi,ss

def get_model(embedding="vlbert"):
    if(embedding=="vlbert"):
        model=VisualBertModel.from_pretrained("uclanlp/visualbert-nlvr2-coco-pre")
    elif(embedding=="clip"):
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    elif(embedding=="bert"):
        model = BertModel.from_pretrained("bert-large-uncased")  
    elif(embedding=="vgg"):
        model = vgg16(pretrained=True)
        model.classifier=nn.Sequential(*list(model.classifier.children())[:-1])      
    model=model.to(device)
    return model

def get_vlbert_embedding(model):
    if not os.path.exists("vl_bert_embeddings"):
        os.mkdir("vl_bert_embeddings")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    for item in annotation["Text"]:
        for file,text in item.items():
            if(file not in pillars):
                continue  
            text = re.sub(r"(?:\@|https?\://)\S+", "", text.lower())
            inputs = tokenizer(text, return_tensors="pt")
            inputs={'input_ids':inputs['input_ids'].to(device),\
                    'token_type_ids':inputs['token_type_ids'].to(device),\
                    'attention_mask':inputs['attention_mask'].to(device)
                }
            with open("./input_embeddings/{}.pkl".format(file),"rb") as f:
                inputs.update(pkl.load(f))
            inputs['input_ids']=inputs['input_ids'].to(device)
            # inputs['token_type_ids']=inputs['token_type_ids'].to(device)
            inputs.pop('token_type_ids')
            inputs['attention_mask']=inputs['attention_mask'].to(device)
            inputs['visual_embeds']=inputs['visual_embeds'].to(device)
            inputs['visual_token_type_ids']=inputs['visual_token_type_ids'].to(device)
            inputs['visual_attention_mask']=inputs['visual_attention_mask'].to(device)
            
            embedding=model(**inputs).last_hidden_state.cpu()[:,0,:] 
            with open("./vl_bert_embeddings/{}.pkl".format(file),"wb") as f:
                pkl.dump(embedding,f)

def get_clip_embedding(model):
    if not os.path.exists("clip_embeddings"):
        os.mkdir("clip_embeddings")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    for item in annotation["Text"]:
        for file,text in item.items():
            if(file not in pillars):
                continue 
            text = re.sub(r"(?:\@|https?\://)\S+", "", text.lower())    
            inputs = processor(text=text,\
                    images=Image.open("./TD_Memes/{}".format(file)),\
                        return_tensors="pt", padding=True)
            inputs={'input_ids':inputs['input_ids'].to(device),'attention_mask':inputs['attention_mask'].to(device),\
                'pixel_values':inputs['pixel_values'].to(device)}
            inputs={
                'input_ids':inputs['input_ids'][:,:77],
                'attention_mask':inputs['attention_mask'][:,:77],
                'pixel_values':inputs['pixel_values']
            }
            outputs=model(**inputs)
            with open("./clip_embeddings/{}.pkl".format(file),"wb") as f:
                pkl.dump(outputs,f)     

def get_bert_embedding(model):
    if not os.path.exists("bert_embeddings"):
        os.mkdir("bert_embeddings")
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
    for item in annotation["Text"]:
        for file,text in item.items():
            if(file not in pillars):
                continue 
            text = re.sub(r"(?:\@|https?\://)\S+", "", text.lower())    
            inputs = tokenizer(text=text,return_tensors="pt", padding=True)
            inputs={'input_ids':inputs['input_ids'].to(device),'attention_mask':inputs['attention_mask'].to(device),\
                'token_type_ids':inputs['token_type_ids'].to(device)}
            outputs=model(**inputs)
            with open("./bert_embeddings/{}.pkl".format(file),"wb") as f:
                pkl.dump(outputs['last_hidden_state'][0,0,:],f) 

def get_vgg_embedding(model):
    if not os.path.exists("vgg_embeddings"):
        os.mkdir("vgg_embeddings")
    transform=transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

    for item in annotation["Text"]:
        for file,text in item.items():
            if(file not in pillars):
                continue 
            img=PIL.Image.open("./TD_Memes/{}".format(file)).convert('RGB')
            img=transform(img).to(device)
            encoding=model(img.unsqueeze(0)).view(-1,4096)
            with open("./vgg_embeddings/{}.pkl".format(file),"wb") as f:
                pkl.dump(encoding,f)

if __name__ == '__main__':
    model=get_model("vlbert")
    get_vlbert_embedding(model)
    nmi,ss=run_kmeans("vlbert")
    print("Visual Bert :\n")
    print("NMI:{} Silhoutte Score:{}".format(nmi,ss))

    model=get_model("clip")
    get_clip_embedding(model)
    nmi,ss=run_kmeans("clip")
    print("CLIP :\n")
    print("NMI:{} Silhoutte Score:{}".format(nmi,ss))

    model=get_model("bert")
    get_bert_embedding(model)
    nmi,ss=run_kmeans("bert")
    print("BERT :\n")
    print("NMI:{} Silhoutte Score:{}".format(nmi,ss))

    model=get_model("vgg")
    get_vgg_embedding(model)
    nmi,ss=run_kmeans("vgg")
    print("VGG :\n")
    print("NMI:{} Silhoutte Score:{}".format(nmi,ss))

