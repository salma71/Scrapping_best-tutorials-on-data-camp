# In this tutorial, I am going to scrape the tutorials section of the DataCamp website 
# and try to get some insights.

# import important libraries

from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.parser import parse
import time
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

# specifiying the URL to scrape

url = 'https://www.datacamp.com/community/tutorials'

# we need to identify how many pages we can query 
# we loop over and find all a-tags and return their number.
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser') # add html.parser feature to surpass warning in the terminal

page = [i.text for i in soup.find_all('a') if 'community/tutorials?page=' in str(i)]
last_page = page[-1]

print(last_page)
# 25

# for each card, we have 

# tag, a, description, author, upvote, social-media, date
# I will initialize then as an empty array

tag = []
link  = []
title =  []
description = []
author = []
date = []
upvotes = []

for page in np.arange(1, int(last_page)+1):
    base_url = 'https://www.datacamp.com'
    url = 'https://www.datacamp.com/community/tutorials?page=' + str(page)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    tag.append([i.text for i in soup.find_all(
        class_='jsx-1764811326 Tag')])  #ok
    title.append([i.text for i in soup.find_all(class_='jsx-379356511 blue')]) #ok
    description.append([i.text for i in soup.find_all(class_='jsx-379356511 blocText description')])#ok
    author.append([i.text for i in soup.find_all(class_='jsx-566588255 name')])#ok
    date.append([i.text for i in soup.find_all(class_='jsx-566588255 date')])#ok
    upvotes.append([i.text for i in soup.find_all(
        class_='jsx-1972554161 voted')]) #ok
    link.append(base_url + i.get('href') for i in soup.find_all(
        'a', class_='jsx-379356511'))  # ok fetch - need to append to base url

    # for i in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    #         link.append(i.get('href'))


# unpack the list of lists using itertools pakage
chain_link = itertools.chain.from_iterable(link)
link_flatted = list(chain_link)

chain_title = itertools.chain.from_iterable(title)
title_flatted = list(chain_title)

chain_tag = itertools.chain.from_iterable(tag)
tag_flatted = list(chain_tag)

chain_author = itertools.chain.from_iterable(author)
author_flatted = list(chain_author)

chain_desc = itertools.chain.from_iterable(description)
desc_flatted = list(chain_desc)

chain_upvote = itertools.chain.from_iterable(upvotes)
upvote_flatted = list(chain_upvote)

chain_date = itertools.chain.from_iterable(date)
date_flatted = list(chain_date)

# save what we got on a csv file 
print(len(link_flatted), len(title_flatted), len(tag_flatted), len(author_flatted), len(desc_flatted), len(upvote_flatted), len(date_flatted))
# 0 67 134 67 67 67 67 -> fetching unexistence tags -> need to make tag list to have the same length of other lists

# We can write a function to pad the shortest lists with empty elements

def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list


tutorial = {
    "title": title_flatted,
    "tag": tag_flatted[:len(title_flatted)],
    "description": desc_flatted,
    "link": link_flatted,
    "voting": upvote_flatted,
    "author": author_flatted,
    "date": date_flatted
}

new_list = pad_dict_list(tutorial, len(title_flatted))
# print(new_list)
df  = pd.DataFrame(new_list)

df.to_csv("/Users/salmaelshahawy/Desktop/Scrapping_best-tutorials-on-data-camp/tutorial_csv.csv", header = True, index = True)
