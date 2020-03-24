import pandas as pd
import io
import matplotlib.pyplot as plt
import math
import nltk
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter

excel_file_path = 'conversations.xlsx'
xls = pd.ExcelFile(excel_file_path)


# Function to visualize word frequency of customers
def plotWordFrequency(sheet, column, plot_title, additional_unnecessary_words=None):
    if additional_unnecessary_words is None:
        additional_unnecessary_words = []

    df = pd.read_excel(xls, sheet)
    df[column] = df[column].str.lower()
    word_count = df.customer.str.split(expand=True).stack().value_counts()

    # read stop words from file
    with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
        vn_stopwords = my_file.read()
    vn_stopwords = vn_stopwords.splitlines()

    unnecessary_words = ['url', 'u', 'e', 'o', 'a', 'i', 'c', 'b', 'la', 'giup', 'oi', 'gui', 'nhg', 'chi', 'minh',
                         'shop',
                         'lam', 'tam', 'nhat', 'dung', 'mua', 'co', 'ko',
                         'a?',
                         'ko?', 'ok', '1', '2', '3', '4', 'dc', 'ạ?', ]
    all_unnecessary_words = vn_stopwords + unnecessary_words + additional_unnecessary_words

    # remove all unnecessary words from word_count
    word_count = word_count.drop(all_unnecessary_words, errors='ignore')
    word_count = word_count[word_count > 3]

    # word_count.hist()
    word_count.plot.barh()
    plt.suptitle(plot_title)
    plt.ylabel('Words')
    plt.yticks(fontsize=8)
    plt.xlabel('Frequency')
    plt.figure(figsize=(10, 100))
    plt.show()


def tfidf_word_unigram(sheet, plot_title, additional_unnecessary_words=None):
    if additional_unnecessary_words is None:
        additional_unnecessary_words = []

    df = pd.read_excel(xls, sheet)
    # read stop words from file
    with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
        vn_stopwords = my_file.read()
    vn_stopwords = vn_stopwords.splitlines()

    unnecessary_words = ['url', 'u', 'e', 'o', 'a', 'i', 'c', 'b', 'la', 'giup', 'oi', 'gui', 'nhg', 'chi', 'minh',
                         'shop',
                         'lam', 'tam', 'nhat', 'dung', 'mua', 'co', 'ko',
                         'a?',
                         'ko?', 'ok', '1', '2', '3', '4', 'dc', 'ạ?', '-', ' ', '😄', '😘', 'vg', 'vâng', '&', '4h',
                         '50', 'nhan', 'bi', 'ngo', 'gau', 'k', 'cn']
    all_unnecessary_words = vn_stopwords + unnecessary_words + additional_unnecessary_words
    
    # handle shop column
    df['shop'] = df['shop'].str.lower()
    word_count_shop = df.shop.str.split(expand=True).stack().value_counts()
    word_count_shop = word_count_shop.drop(all_unnecessary_words, errors='ignore')
    word_count_shop = word_count_shop[word_count_shop > 2]

    # handle customer column
    df['customer'] = df['customer'].str.lower()
    word_count_customer = df.customer.str.split(expand=True).stack().value_counts()
    # remove all unnecessary words from word_count
    word_count_customer = word_count_customer.drop(all_unnecessary_words, errors='ignore')
    word_count_customer = word_count_customer[word_count_customer > 2]

    # calculate tf and idf for customer and shop
    tf_customer = {}
    tf_shop = {}
    idf_customer = {}
    idf_shop = {}

    word_count_customer_sum = sum(word_count_customer)
    word_count_shop_sum = sum(word_count_shop)
    for index, row in word_count_customer.items():
        tf = row / word_count_customer_sum
        tf_customer.update({index: tf})
        document_contains_word = 1
        if index in word_count_shop:
            document_contains_word = 2
        idf = math.log(2 / document_contains_word)
        idf_customer.update({index: idf})

    for index, row in word_count_shop.items():
        tf = row / word_count_shop_sum
        tf_shop.update({index: tf})
        document_contains_word = 1
        if index in word_count_customer:
            document_contains_word = 2
        idf = math.log(2 / document_contains_word)
        idf_shop.update({index: idf})
    x = 0


def calculateAverageWaitTime(sheet, plot_title, max_time=9999999999):
    df = pd.read_excel(xls, sheet)

    # Get stl column data
    customer_wait_time = df.loc[df['label'] == "Shop Gấu & Bí Ngô - Đồ dùng Mẹ & Bé cao cấp", 'stl']
    customer_wait_time = customer_wait_time[
        customer_wait_time <= max_time]  # remove periods that are too big in difference with the rest

    average_wait_time = customer_wait_time.mean()
    average_wait_time = round(average_wait_time, 2)

    customer_wait_time_with_date = df.loc[
        df['label'] == "Shop Gấu & Bí Ngô - Đồ dùng Mẹ & Bé cao cấp", ['fixed_time', 'stl']]
    customer_wait_time_with_date = customer_wait_time_with_date[
        customer_wait_time_with_date['stl'] <= max_time]  # remove periods that are too big in difference with the rest

    # customer_wait_time_with_date.plot(x='fixed_time', y='stl')
    customer_wait_time_with_date.plot.scatter(x='fixed_time', y='stl', c="DarkBLue")
    plt.suptitle(plot_title)
    plt.xlabel('Date')
    plt.ylabel('Wait time (seconds)')
    plt.figtext(.55, .8, "Average Wait Time:" + str(average_wait_time) + "s")
    plt.xticks(rotation=35)
    plt.show()


df = pd.read_excel(xls, '0')
df['customer'] = df['customer'].str.lower()

additional_unnecessary_words = ['t', 'có', 'nhé', 'ko', 'cho', 'ơi', 'mình', 'này', 'lấy', 'k', 'còn',
                                'bạn',
                                'bn', 'tớ', 'thanh', 'm', 'là', '.', 'ah', 'làng', 'dãy', 'đi', 'báo', 'máy', 'châu',
                                'giúp',
                                '15', 'ui', 'nhá', 'quây', 'j', 'x', 'bên', 'cái', 'ah', 'luôn', '2', 'nữa', 'số',
                                'ntnao',
                                'dchi', 'ơn', 'r', 'km', 'kia', 'trc', '1m32', 'pha', 'góc', 'í', '-', '?', 'sz', 'sợ',
                                'oki',
                                '0936875999', '+', 'hình', 'ck', 'alo', 'mấy', 'hộ', 'món', 'kệ', 'cảm', '&', 'ngô',
                                'bí',
                                'nhé.', 'hà', 'việt', 'đồ', 'âu', 'thước', '16a7', '1c', 'hả', 'kích']
tfidf_word_unigram('0', 'Word Frequency Customer 1 ')

#
plotWordFrequency('0', 'customer', 'Word Frequency Customer 1 ')
plotWordFrequency('1', 'customer', 'Word Frequency Customer 2', additional_unnecessary_words)
#
calculateAverageWaitTime('0', "Customer 1 wait time", 3977)
calculateAverageWaitTime('1', "Customer 2 wait time", 14291)

df = pd.read_excel(xls, '0')
bigram_words_customer = []
bigram_words_shop = []
for index, row in df.customer.iteritems():
    if pd.isna(row) == False:
        words = row.split()
        bigram_words_customer += (list(map(' '.join, zip(words[:-1], words[1:]))))

for index, row in df.shop.iteritems():
    if pd.isna(row) == False:
        words = row.split()
        bigram_words_shop += (list(map(' '.join, zip(words[:-1], words[1:]))))

bigram_words_customer_counter = Counter(bigram_words_customer).most_common()
bigram_words_shop_counter = Counter(bigram_words_shop).most_common()
