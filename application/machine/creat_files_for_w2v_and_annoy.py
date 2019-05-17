from functools import lru_cache
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import tqdm
import pickle as pkl
import pymorphy2
import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from gensim.models.word2vec import Word2Vec
from nltk.tokenize import word_tokenize

MORPH = pymorphy2.MorphAnalyzer()
porter = PorterStemmer()


def creat():
    data = __create_data_frame__()
    __create_w2v__(data)
    __create_annoy__(data)
    return data


def __create_data_frame__():
    data = pd.read_csv('article_from_db.csv')
    columns = ['authors', 'title', 'ref',
               'annotation', 'key_words']
    delete_columns = [column not in columns for column in data.columns]
    data = data.drop(columns=data.columns[delete_columns])
    data = data.fillna(" ")
    data['Title'] = data['title'].apply(lambda x: __normalize_text__(x))
    data['Description'] = data['annotation'].apply(
        lambda x: __normalize_text__(x))
    data['Key words'] = data['key_words'].apply(
        lambda x: __normalize_text__(x))
    return data


def __create_w2v__(data):
    sentences = (data['Title'] + ' ' + data[
        'Description']).str.split()
    model = Word2Vec(sentences, size=100, workers=2, iter=15)
    model.save('./w2v_products.w2v_gensim')


def __create_annoy__(data):
    model = Word2Vec.load('./w2v_products.w2v_gensim')

    titles_ = (data['Title'] + ' ' + data['Description']).values

    tfidf = TfidfVectorizer(ngram_range=(1, 1))
    tfidf.fit(titles_)

    # tf_idf_vocab = {}
    # for i in model.wv.vocab.keys():
    #     if i in tfidf.vocabulary_:
    #         tf_idf_vec = tfidf.transform([i])
    #         tf_idf_vocab[i] = \
    #             tf_idf_vec[:, tfidf.vocabulary_[i]].toarray().flatten()[0]

    tf_idf_vocab = {}
    for i in model.wv.vocab.keys():
        if i in tfidf.vocabulary_:
            tf_idf_vocab[i] = tfidf.idf_[tfidf.vocabulary_[i]]

    data_storage = {i[0]: i[1]['title'] + ' ' + i[1]['annotation'] for
                    i in data.iterrows()}
    data_storage_norm = {}
    for i in tqdm.tqdm(data_storage):
        text = __normalize_text__(data_storage[i])
        vec = np.zeros(100)
        for word in text.split(' '):
            if word in model and word in tf_idf_vocab:
                vec += model[word] * tf_idf_vocab[word]
        data_storage_norm[i] = vec

    num_trees = 15
    vec_size_emb = 100

    counter = 0
    map_id_2_prod_hash = {}
    index_title_emb = AnnoyIndex(vec_size_emb)

    for prod_hash in data_storage_norm:
        title_vec = data_storage_norm[prod_hash]

        index_title_emb.add_item(counter, title_vec)

        map_id_2_prod_hash[
            counter] = prod_hash

        counter += 1

    index_title_emb.build(num_trees)
    index_title_emb.save('./annoy')
    pkl.dump(map_id_2_prod_hash, open('map_id_to_hash_products.dict', 'wb'))


@lru_cache(maxsize=100000)
def __get_normal_form__(i):
    return porter.stem(i.lower())


def __normalize_text__(text):
    stop_words = list(stopwords.words('english'))
    text = text[:text.find('©')]
    tokens = word_tokenize(text)
    text = [word for word in tokens if word.isalpha()]
    normalized = [__get_normal_form__(word) for word in text]
    return ' '.join([word for word in normalized if word not in stop_words])
