import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt


def plotWordFrequency(excel_file_path, sheet, column, plot_title, additional_unnecessary_words=None):
    if additional_unnecessary_words is None:
        additional_unnecessary_words = []
    xls = pd.ExcelFile(excel_file_path)
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
    all_stopwords = vn_stopwords + unnecessary_words + additional_unnecessary_words

    # remove stop word from word_count
    word_count = word_count.drop(all_stopwords, errors='ignore')
    word_count = word_count[word_count > 3]

    # word_count.hist()
    word_count.plot.barh()
    plt.suptitle(plot_title)
    plt.ylabel('Words')
    plt.yticks(fontsize=8)
    plt.xlabel('Frequency')
    plt.figure(figsize=(10, 100))
    plt.show()


additional_unnecessary_words = ['action_outside', 't', 'có', 'nhé', 'ko', 'cho', 'ơi', 'mình', 'này', 'lấy', 'k', 'còn',
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
#
plotWordFrequency('conversations.xlsx', '0', 'customer', 'Customer Conversation 1')
plotWordFrequency('conversations.xlsx', '1', 'customer', 'Customer Conversation 2', additional_unnecessary_words)
