import pandas as pd
import numpy as np
import io

df = pd.read_excel(r'C:\Users\ngduc\Downloads\conversations\conversations\conversations.xlsx')
print(df)
df['customer'] = df['customer'].str.lower()
word_count = df.customer.str.split(expand=True).stack().value_counts()
print(word_count)

# read stop words from file
with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
    vn_stopwords = my_file.read()
vn_stopwords = vn_stopwords.splitlines()

# remove stop word from word_count
word_count = word_count.drop(vn_stopwords, errors='ignore')
word_count = word_count[word_count > 2]
b = 0
