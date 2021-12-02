#!/usr/bin/python
# -*- coding: utf-8 -*-
# merge the different .csv file under "data/meta/" into a big papers_meta.csv file, using pandas
# author: Dai Yao (www.yaod.ai; DAI@yodadai.com)
# date: 2021/12/02

import pandas as pd
import re

pages = range(0, 69)
print(pages)

all_papers = pd.DataFrame()


def get_year(ym):
    ''' given a string [ym], retrieve the year information '''
    year = -1
    match = re.match(r'.*([1-3][0-9]{3})', ym)
    if match is not None:
        # Then it found a match!
        year = match.group(1)
    return year


for page in pages:
    papers = pd.read_csv('data/meta/papers_meta_' + str(page) + '.csv', header=0)
    papers['year'] = papers['ym'].apply(lambda x: get_year(x))

    frames = [all_papers, papers]
    all_papers = pd.concat(frames)
    print(all_papers.shape)

all_papers.to_csv('data/papers_meta.csv', index=False)
