import pandas as pd
import io
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import plotly.express as px

import matplotlib.pyplot as plt
import math
import nltk
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter


def remove_unnecessary_words(text, all_unnecessary_words):
    text_words = text.split()
    result_words = [word for word in text_words if word not in all_unnecessary_words and word.isalpha() == True]
    result = ' '.join(result_words)
    if result == '':
        result = np.nan
    return result


def pre_process():
    # read stop words from file
    with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
        vn_stopwords = my_file.read()
    vn_stopwords = vn_stopwords.splitlines()

    unnecessary_words = ['url', 'u', 'e', 'o', 'a', 'i', 'c', 'b', 'la', 'giup', 'oi', 'gui', 'nhg', 'chi', 'minh',
                         'shop',
                         'lam', 'tam', 'nhat', 'dung', 'mua', 'co', 'ko',
                         'a?',
                         'ko?', 'ok', '1', '2', '3', '4', 'dc', 'ạ?', 'uki', 'uh', 'alo', 'okie', 'thks']
    all_unnecessary_words = vn_stopwords + unnecessary_words
    customer_message = df['customer'].str.lower()
    customer_message = customer_message.drop(all_unnecessary_words, errors="ignore")
    customer_message = customer_message.dropna()
    customer_message = customer_message.apply(lambda row: remove_unnecessary_words(row, all_unnecessary_words))
    customer_message = customer_message.dropna().reset_index(drop=True)
    return customer_message


excel_file_path = 'conversations.xlsx'
xls = pd.ExcelFile(excel_file_path)
df = pd.read_excel(xls, '0')

customer_message = pre_process()

documents = customer_message.tolist()

# calculate term frequency
vectorizer = CountVectorizer()
vectorizer.fit(documents)
vector = vectorizer.fit_transform(documents)
# pd.DataFrame(vector.toarray(),columns=vectorize.get_feature_names())

# calculate idf
tfidf_transformer = TfidfTransformer()

tfidf_transformer.fit(vector)

# calculate tf-idf
all_lines = ''
for index, line in customer_message.items():
    all_lines += line + ' '

tfidf_vector = tfidf_transformer.transform(vectorizer.transform([all_lines]))

tfidf_dataframe = pd.DataFrame(tfidf_vector.toarray(), index=['tfidf'])
tfidf_dataframe = tfidf_dataframe.transpose()
tfidf_dataframe['words'] = vectorizer.get_feature_names()
tfidf_dataframe = tfidf_dataframe.sort_values(by='tfidf', ascending=False)[['words', 'tfidf']]

fig = px.bar(tfidf_dataframe, x=tfidf_dataframe['tfidf'], y=tfidf_dataframe['words'],
             color=tfidf_dataframe['tfidf'],
             orientation='h', height=600)
fig.show()
