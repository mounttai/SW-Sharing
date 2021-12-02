#!/usr/bin/python
# -*- coding: utf-8 -*-
# download the abstract of each paper - page by page, altogether 68 pages.
# author: Dai Yao (www.yaod.ai; DAI@yodadai.com)
# date: 2021/12/02

import random

import requests
from bs4 import BeautifulSoup
import time

import pandas as pd

pages = range(1, 2)
print(pages)

main_url = 'https://pubsonline.informs.org'

for page in pages:
    print('>>>>>>>> ' + str(page))
    papers = pd.read_csv('data/meta/papers_meta_'+str(page)+'.csv', header=0)

    papers_data = []

    for i in range(papers.shape[0]):
    #for i in range(5):
        paper_link = papers.loc[i].link
        paper_url = main_url + paper_link
        print(str(i) + ': ' + paper_url)
        soup = BeautifulSoup(
            requests.get(paper_url, allow_redirects=True).content, features="html.parser")

        if not (paper_link == "/doi/10.1287/msom.2021.0998" or
                paper_link == "/doi/10.1287/inte.2019.0994"):
            abstract_div = soup.find("div", {"class": "abstractSection abstractInFull"})
            if not abstract_div is None:
                paper_abstract = ''
                txt_divs = abstract_div.find_all(text=True, recursive=True)
                for txt_div in txt_divs:
                    paper_abstract = paper_abstract + ' ' + txt_div.strip()
                papers_data.append([papers.loc[i].link, paper_abstract])

        # sleep for 3 seconds every 10 downloads
        rnd1 = random.randint(1,5)
        rnd2 = random.randint(1,10)
        if i % rnd1 == 0:
            time.sleep(rnd2)

    papers_abstract = pd.DataFrame(
        data=papers_data, columns=['link', 'abstract'])
    papers_abstract.to_csv('data/abstract/papers_'+str(page)+'.csv', index=False)

    if page % 5 == 0:
        time.sleep(10)
