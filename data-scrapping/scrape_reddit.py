import os
import requests
import json 
import argparse
import datetime
import pandas as pd
from tqdm import tqdm
import re

class MemeScrapper():
    
    
    def __init__(self, config):
    
        self.config = config
        
        # create directory structure 
        self.config.images_dir = os.path.join(os.getcwd(), "data", self.config.subreddit, self.config.images)
        self.config.meta_dir = os.path.join(os.getcwd(), "data", self.config.subreddit, self.config.meta)
        
        # make dirs
        try:
            os.makedirs(self.config.images_dir, exist_ok=True)
        except OSError as error:
            print("Directory '%s' can not be created" %self.config.images_dir)
            
        try:
            os.makedirs(self.config.meta_dir, exist_ok=True)
        except OSError as error:
            print("Directory '%s' can not be created" %self.config.meta_dir)
            
        # hard coded meta data to fetch scrap
        self.meta = [
            'allow_live_comments', 'author', 'author_premium', 'can_mod_post', 'contest_mode', 'created_utc',
            'full_link', 'id', 'is_crosspostable', 'is_meta', 'is_original_content', 'is_self', 'is_video',
            'link_flair_text', 'locked', 'media_only', 'no_follow', 'num_comments', 'num_crossposts', 'over_18',
            'parent_whitelist_status', 'permalink', 'pinned', 'score', 'selftext', 'send_replies', 'spoiler',
            'stickied', 'title', 'total_awards_received', 'url'
        ]
        
        self.valid_extns = ["jpg", "jpeg", "png", "gif", "JPG", "JPEG", "PNG", "GIF"]

        
    
        
    def download_and_save_image(self, url):
        """method to download and save image locally

        Args:
            image (dict): dictionary which should have image url and path where to save downloaded image. 
        """
        try:
            response = requests.get(url)
        except:
            return False
        
        image_name = url.split("/")[-1]
        
        
        # validate the name and url 
        if len(image_name)!=0 and response.status_code==200:
            
            # get only .jpg, .jpeg .png and .gif files
            # get only .jpg, .jpeg .png and .gif files
            extn = image_name.split(".")[-1]
           
            
            if extn in self.valid_extns:
                # get the path
                image_path = os.path.join(self.config.images_dir, image_name)
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                return True
            
        elif response.status_code==404:
            return False
        else:
            return False
        return False
        
        
    
    
    def pushshiftAPICall(self, before, after, subreddit, query=""):
        
        url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=2000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(subreddit)
        
        r = requests.get(url)
        data = json.loads(r.text)
        return data['data']

    
    
    def scrape_subreddit(self):
        """
            method to scrap a particular subreddit within a specified time. 
        """  
        
        subCount = 0
        subStats = {}  
            
        
        
        data = self.pushshiftAPICall(after=self.config.after, before=self.config.before, subreddit=self.config.subreddit, query="")
        
        # Will run until all posts have been gathered 
        # from the 'after' date up until before date
        while len(data) > 0:
            
            for submission in tqdm(data):
                # extracting all information about a submission
                meta_data = [submission.get(key) for key in self.meta]    
                
                # download and save image
                flag = self.download_and_save_image(submission['url'])
                
                # only if image has not been deleted
                if flag:
                    subStats[submission.get('id')] = meta_data
                    subCount+=1
                else:
                    continue
                
            # Calls getPushshiftData() with the created date of the last submission
            # print(len(data))
            if subCount % 1000 == 0:
                print(f'{subCount} submission collected')
                
            print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = self.pushshiftAPICall(after=after, before=self.config.before, subreddit=self.config.subreddit, query="")
            
        
        # save meta data as csv file
        df = pd.DataFrame(data=list(subStats.values()), columns = self.meta, index=None)
        
        file_name = os.path.join(self.config.meta_dir, "meta.csv")
        
        df.to_csv(file_name, index=False)
        
        before_datetime = str(datetime.datetime.fromtimestamp(int(self.config.before)))
        after_datetime = str(datetime.datetime.fromtimestamp(int(self.config.after)))
        
        
        print(f'\nMemes scrapped from r/{self.config.subreddit} submitted between %s and %s'%( before_datetime, after_datetime))
        print(f'\nImages are saved at %s and meta data is stored at %s\n'%(self.config.images_dir, self.config.meta_dir))
        
    
    def start(self):
        self.scrape_subreddit()
            
       

def main():
    
    parser = argparse.ArgumentParser(description='Meme Scrapper from Reddit.')
    
    required_args = parser.add_argument_group('required arguments')
    
    required_args.add_argument('--subreddit', type=str, dest='subreddit', help="Which subreddit to scrap?", required=True)
    required_args.add_argument('--after', type=str,dest='after', help="Unix timestamp after which to scrap images?", required=True)
    required_args.add_argument('--before', type=str, dest='before', help="Unix timestamp before which to scrap images?", required=True)
    required_args.add_argument('--images', type=str,dest='images', help="Where to save images?", default="images", required=False)
    required_args.add_argument('--meta', type=str,dest='meta', help="Where to save metadata?", default="meta", required=False)

    args = parser.parse_args()
    
    scraper = MemeScrapper(config=args)
    scraper.start()
    
    # print(len(data))


if __name__ == '__main__':
    main()