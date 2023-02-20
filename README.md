
## Rum 
<br/>
Multi-modal meme analysis

## File Summary
* postprocessing/processing.ipynb - de-duplication, corrupt file filtering and prioritization
* clustering.ipynb - clustering on extracted embeddings
* classification.ipynb - pillar-stance classification using MLP on top of embeddings
* report/report.py - annotation agreement\conflict analysis.
* postprocessing/priority_memes.csv - prioritized memes
* report/annotated_memes.json - annotated visuals <br/>
non-memes      - Id,Filename <br/>
memes          - Id,Filename <br/>
non sg memes   - Id,Filename <br/>
SG memes       - Id,Filename <br/>
meme text      - OCR extracted text from the memes <br/>
pillar_matches - list of memeid,pillars <br/>
stance_matches - meme ids where stance match <br/>
matched_memes  - details of agreement memes(memeId,Filename,relatedCountry,pillars,stances)


## Annotation summary
We annotate a subset of 7,200 visuals from priority memes. <br/>
Each visual is assigned following labels: <br/>
<ol>
    <li> Meme/Non-Meme - binary </li>
    <li> SG/Non-SG     - binary </li>
    <li> pillars       - multi choice (6 total defence pillars + 'others') </li>
    <li> stance        - one out of 3 (supportive,neutral,against) </li>
    <li> tags          - hashtags to describe a meme (min length - , max length - , mean length - ) </li>
</ol>

|               | Count          |
| ------------- | -------------  |
| Non-meme      | 1,711          |
| Meme          | 5,401          |
| Non-SG meme   | 2,408          |
| SG Meme       | 2,893          |
| Pillars       | 2,513          |
| Stance        | 1,876          |


## Dataset
* data is available at - https://drive.google.com/file/d/1aFXF8ePvY-d2cBjKfH-MiAj_dqGhcHog/view?usp=sharing

|               | Count         |
| ------------- | ------------- |
| Google search | 2,125         |
| Instagram     | 33,954        |
| Total         | 36,079        |


Instagram handles - <br/>
#mindefmemes <br/>
@kmfst_ <br/>
@memedefsg <br/>
@sgagsg <br/>
#sgmeme <br/>
#sgmemes <br/>
#singaporememes <br/>
@yeolo.sg <br/>
@mndsg_ (memes n dreams singapore) <br/>
@nus_memes <br/>
@smumemes <br/>
@pioneer_university <br/>
@changicollege <br/>
@sginsurancememes <br/>
@sgsocialworkmemes <br/>
@mas_complaints <br/>
@sit.tum.memes <br/>
#sgmemes

## Data Collection
* data-scraping/google_search_crawler.py - Data is collected form google search using keywords for each of the 6 pillars <br/>
* data-scraping/scrape_reddit.py - reddit scrape with inputs - subreddit,before and after timestamp <br/>
* To scrape instagram, we use instaloader library(https://pypi.org/project/instaloader/) <br/>
    usage - instaloader profile [instagram page handle e.g. memedefsg] <br/>
    This creates a folder with the handle name and downloads visuals <br/>

## Installation
* data scraping from google - pip install simple-image-download <br/>
* data scraping from instagram - pip install instaloader

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
