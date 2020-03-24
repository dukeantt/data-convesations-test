import pandas as pd
import io
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import plotly.express as px


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


def tfidf_calculator(count_vectorizer, tfidf_transformer, documents):
    # calculate term frequency
    count_vectorizer.fit(documents)
    vector = count_vectorizer.fit_transform(documents)
    # pd.DataFrame(vector.toarray(),columns=vectorize.get_feature_names())

    # calculate idf
    tfidf_transformer.fit(vector)


excel_file_path = 'conversations.xlsx'
xls = pd.ExcelFile(excel_file_path)
df = pd.read_excel(xls, '0')
customer_message = pre_process()
documents = customer_message.tolist()

vectorizer = CountVectorizer()
tfidf_transformer = TfidfTransformer()
tfidf_calculator(vectorizer, tfidf_transformer, documents)

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

bigram_vectorizer = CountVectorizer(ngram_range=(2, 2))
bigram_tfidf_transformer = TfidfTransformer()
tfidf_calculator(bigram_vectorizer, bigram_tfidf_transformer, documents)
bigram_tfidf_vector = bigram_tfidf_transformer.transform(bigram_vectorizer.transform([all_lines]))

bigram_tfidf_dataframe = pd.DataFrame(bigram_tfidf_vector.toarray(), index=['tfidf'])
bigram_tfidf_dataframe = bigram_tfidf_dataframe.transpose()
bigram_tfidf_dataframe['words'] = bigram_vectorizer.get_feature_names()
bigram_tfidf_dataframe = bigram_tfidf_dataframe.sort_values(by='tfidf', ascending=False)[['words', 'tfidf']]

fig = px.bar(bigram_tfidf_dataframe, x=bigram_tfidf_dataframe['tfidf'], y=bigram_tfidf_dataframe['words'],
             color=bigram_tfidf_dataframe['tfidf'],
             orientation='h', height=600)
fig.show()