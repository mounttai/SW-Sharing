#!/usr/bin/python
# -*- coding: utf-8 -*-
# download the meta data for all the papers from searching "sharing economy", page by page, all 68 pages.
# author: Dai Yao (www.yaod.ai; DAI@yodadai.com)
# date: 2021/12/02

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import time

import pandas as pd

pages = range(69)
print(pages)

main_url = 'https://pubsonline.informs.org/action/doSearch?AllField=sharing+economy&ContentItemType=research-article'

for page in pages:
    papers_data = []
    page_url = main_url + '&startPage=' + str(page) + '&pageSize=100'
    print(page_url)
    soup = BeautifulSoup(
        requests.get(page_url, allow_redirects=True).content, features="html.parser")
    item_divs = soup.find_all("div", {"class": "item__body"})
    for item_div in item_divs:
        title_field = item_div.find("h5", {"class": "hlFld-Title meta__title meta__title__margin"})
        paper_link = title_field.find('a')['href']
        paper_title = title_field.find('a').contents[0]
        #print(paper_link + ", " + paper_title)
        if not (paper_title == "About Our Authors" or
                paper_title == "Focus On Authors" or
                paper_title == "Research Spotlights" or
                paper_title == "Editorial Statement—Operations Management" or
                paper_title == "Managers, Computer Systems, and Productivity—Franz Edelman, in Memoriam" or
                paper_title == "Awful August?"):
            author_fields = item_div.find_all("ul", {"class": "meta__authors rlist--inline"})
            paper_authors = ""
            for author_field in author_fields:
                paper_authors = author_field.find('a').contents[0] + "; "
            # print(paper_authors)
            journal_field = item_div.find("div", {"class": "meta__details"})
            paper_journal = journal_field.find('a').contents[0]
            paper_ym = journal_field.find('span').contents[0]
            # print(paper_journal + ", " + paper_ym)

            # add the record
            papers_data.append([paper_link, paper_title, paper_authors, paper_journal, paper_ym])

    papers = pd.DataFrame(
        data=papers_data, columns=['link', 'title', 'authors', 'journal', 'ym'])
    papers.to_csv('data/meta/papers_meta_'+str(page)+'.csv', index=False)

    if page % 5 == 0:
        time.sleep(10)