# ## Yelp Reviews
# This project aims to extract reviews for SoFi Stadium from Yelp and utilize Natural Language Processing (NLP)
# techniques on the data to gain insights into customer sentiment and opinion. The Yelp reviews will be scraped, 
# parsed, and cleaned to obtain the relevant information. The data will be analyzed using various NLP techniques
# such as sentiment analysis, topic modeling, and text classification. The results of the analysis will be used
# to identify the most popular topics discussed in the reviews, the overall sentiment towards the stadium, and 
# any areas of improvement that can be identified. The insights obtained from this project will help SoFi Stadium 
# improve its services and better meet customer expectations.

#!/Users/itysoni/opt/anaconda3/bin/python

## Import required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json
import os


## Initialize header
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}


def parse_url(url='https://www.yelp.com/biz/sofi-stadium-inglewood?osq=sofi+stadium', out_file='yelp_reviews.csv') :
    '''
    This function get the data from url and pareses the html content and adds the information 
    (author, date, rating, and review) in out_file if the information isn't present already
    '''
    data_dicts=[]
    out_file='yelp_reviews.csv'
    for i in range(0,1):
        nextpage_url = url+'&start='+str(i*10)  ## Next page url
        nextpage=requests.get(nextpage_url,headers=headers) 
        soup = BeautifulSoup(nextpage.content, 'html.parser')  ## Get data from the url 
        body=soup.find('div')
        data_tmp=body.find_all('script',type="application/ld+json")
        data_dicts.extend(json.loads(data_tmp[1].string)['review'])  ## Find information related to reviews
    df=pd.DataFrame(data_dicts)
    if os.path.isfile(out_file):  ## Read the data if the file already exists
        d=pd.read_csv(out_file, index_col=False)  
        df=pd.concat([df,d])   ## combine the old and new data
        df['reviewRating'] = df['reviewRating'].astype(str)  
        df.drop_duplicates(ignore_index=True, inplace=True)  ## remove dulicate entries from the df
    df.to_csv(out_file, mode='w', index=False)  ## Write df to out_file


if __name__ == "__main__":
    parse_url()

