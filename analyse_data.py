import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\ngduc\Downloads\conversations\conversations\conversations.xlsx')
print(df)
df['customer'] = df['customer'].str.lower()
word_count = df.customer.str.split(expand=True).stack().value_counts()
print(word_count)

# read stop words from file
with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
    vn_stopwords = my_file.read()
vn_stopwords = vn_stopwords.splitlines()
stopwords = ['url','u','e','o','a','i','c','minh','shop','lam','tam','nhat','dung','mua','co','ko','a?','ko ?','ok','1','2','3','4']
all_stopwords = vn_stopwords + stopwords
# remove stop word from word_count
word_count = word_count.drop(all_stopwords, errors='ignore')
word_count = word_count[word_count > 3]


# word_count.hist()
word_count.plot.barh()
plt.ylabel('Words')
plt.yticks(fontsize=8)
plt.xlabel('Frequency')
plt.figure(figsize=(10,100))
plt.show()
