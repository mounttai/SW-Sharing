#!/usr/bin/python
# -*- coding: utf-8 -*-
# create the word cloud for all the papers on "social economy",
# as well as that for all the papers on the topic from different journals
# and/or in different years - which is done manually
# author: Dai Yao (www.yaod.ai; DAI@yodadai.com)
# date: 2021/12/02

import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("data/papers_meta.csv")

df_mksc = df[df['journal']=="Marketing Science"]
df_mnsc = df[df['journal']=="Management Science"]
df_ogsc = df[df['journal']=="Organization Science"]

df_2010 = df[df['year']==2010]
df_2015 = df[df['year']==2015]
df_2020 = df[df['year']==2020]

stopwords = set(STOPWORDS)
stopwords.update(
    ["research note", "Mean", "Management Science", "Operations Research",
     "Marketing Science", "Study", "Case", "Means"])

text = " ".join(title for title in df.title)
print ("There are {} words in the combination of all review.".format(len(text)))

mask = np.array(Image.open("results/polyu.png"))
wordcloud_sw = WordCloud(
    stopwords=stopwords, background_color="white", max_words=1000, mask=mask).generate(text)

# create coloring from image
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[8,8])
plt.imshow(wordcloud_sw.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")

# store to file
plt.savefig("results/all_wc.png", format="png")