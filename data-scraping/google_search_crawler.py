import tqdm
import os
from simple_image_download import simple_image_download as simp

#what_to_crawl = {
    #"defense":["Singapore air force memes", "Singapore defense memes", "Singapore national service memes", "Singapore military memes", "memedef Singapore", "NSF Singapore memes"],
    #"civil":["Singapore police force memes","singapore police memes", "singapore civil memes"],
    #"economics":["singapore new water memes", "singapore economics memes", "singapore cpf memes", "Singapore HDB memes", "Singapore finance memes"],
    # "economics":["Singapore finance memes"],
    #"social":["Singapore social memes", "Singapore culture memes", "Singapore Immigration memes", "singapore funny memes", "singapore memes", "singapore covid memes", "singapore lockdown memes", "singapore pandemic memes", "singapore food memes"],
    #"psychological":["singapore government memes", "singapore mental health memes"],
    #"digital":["singapore tech memes", "singapore scamming memes", "singapore misinformation memes"]
#}


# new queries as highlighted in the document 
what_to_crawl = {
    "defense":["Singapore air force memes site:reddit.com", "Singapore military memes site:instagram.com"],
    "civil":["Singapore police memes site:reddit.com", "Singapore police memes site:instagram.com"],
    "economics":["Singapore new water memes site:reddit.com", "Singapore finance meme site:reddit.com", "Singapore finance meme site:twitter.com", "Singapore fresh chicken export ban memes"],
    "social":["Singapore racial memes", "Singapore racist memes", "Singapore religion memes", "Singapore religious memes", "Singapore chinese memes", "Singapore indian memes", "Singapore racial memes site:reddit.com", "Singapore racist memes site:reddit.com", "Singapore racist memes site:twitter.com"],
    "psychological":["Singapore government memes site:reddit.com", "Singapore government memes site:twitter.com"],
    "digital":["Singapore tech memes site:reddit.com", "Singapore scamming memes site:twitter.com", "Singapore phishing memes", "Singapore smart nation memes"],
    "others":["Singapore COVID-19 mask memes [COVID-19]", "Singapore COVID-19 memes [COVID-19]", "Singapore tracetogether memes", "Singapore East Coast Memes", "Singapore Heng Swee Heng Memes", "Singapore NDP Memes" "Singapore memes site:reddit.com", "Singapore memes site:twitter.com", "Singapore memes site:instagram.com"]
}




def main():
    
    response = simp.simple_image_download
    
    for domain in tqdm.tqdm(what_to_crawl.keys()):
        
        # # # create directory structure 
        # path = os.path.join(os.getcwd(), "data", "gis", domain)
        # # make dirs
        # try:
        #     os.makedirs(path, exist_ok=True)
        # except OSError as error:
        #     print("Directory '%s' can not be created" %path)
            
            
        # google_crawler = GoogleImageCrawler(storage={'root_dir': path})
        
        for keyword in tqdm.tqdm(what_to_crawl[domain]):
            print(f"Starting to crawl domain: {domain} and keyword: {keyword}")
            
            response().download(keyword, 700)


if __name__ == '__main__':
    main()
		
