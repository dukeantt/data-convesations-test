import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt


def plotWordFrequency(excel_file_path, sheet, column, additional_stop_word=None):
    if additional_stop_word is None:
        additional_stop_word = []
    xls = pd.ExcelFile(excel_file_path)
    df = pd.read_excel(xls, sheet)
    df[column] = df[column].str.lower()
    word_count = df.customer.str.split(expand=True).stack().value_counts()

    # read stop words from file
    with io.open("vn_stopwords.txt", "r", encoding="utf-8") as my_file:
        vn_stopwords = my_file.read()
    vn_stopwords = vn_stopwords.splitlines()
    stopwords = ['url', 'u', 'e', 'o', 'a', 'i', 'c', 'b', 'la', 'giup', 'oi', 'gui', 'nhg', 'chi', 'minh', 'shop',
                 'lam', 'tam', 'nhat', 'dung', 'mua', 'co', 'ko',
                 'a?',
                 'ko?', 'ok', '1', '2', '3', '4', 'dc', 'ạ?', ]
    all_stopwords = vn_stopwords + stopwords + additional_stop_word

    # remove stop word from word_count
    word_count = word_count.drop(all_stopwords, errors='ignore')
    word_count = word_count[word_count > 3]

    # word_count.hist()
    word_count.plot.barh()
    plt.ylabel('Words')
    plt.yticks(fontsize=8)
    plt.xlabel('Frequency')
    plt.figure(figsize=(10, 100))
    plt.show()


additional_stop_word = ['action_outside', 't', 'có', 'nhé', 'ko', 'cho', 'ơi', 'mình', 'này', 'lấy', 'k', 'còn', 'bạn',
                        'bn', 'tớ', 'thanh', 'm', 'là', '.', 'ah', 'làng', 'dãy', 'đi', 'báo', 'máy', 'châu', 'giúp',
                        '15', 'ui', 'nhá', 'quây', 'j', 'x', 'bên', 'cái', 'ah', 'luôn', '2', 'nữa', 'số', 'ntnao',
                        'dchi', 'ơn', 'r', 'km', 'kia', 'trc', '1m32', 'pha', 'góc', 'í', '-', '?', 'sz', 'sợ', 'oki',
                        '0936875999', '+', 'hình', 'ck', 'alo', 'mấy', 'hộ', 'món', 'kệ', 'cảm', '&', 'ngô', 'bí',
                        'nhé.', 'hà', 'việt', 'đồ', 'âu', 'thước', '16a7', '1c', 'hả', 'kích']
plotWordFrequency('conversations.xlsx', '0', 'customer')
plotWordFrequency('conversations.xlsx', '1', 'customer', additional_stop_word)
