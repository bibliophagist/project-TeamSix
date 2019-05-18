from gensim.models import Word2Vec

from application import app
from application.machine import creat_files_for_w2v_and_annoy
import pickle as pkl
from annoy import AnnoyIndex
import itertools
import numpy as np


class Seeker:
    def __init__(self, data=None):
        if data is not None:
            self.data = data
        else:
            self.data = creat_files_for_w2v_and_annoy.creat()

    def find_article_by_text(self, text, checkbox):
        data_storage = {i[0]: i[1]['title'] + ' ' + i[1]['annotation']
                        for i in self.data.iterrows()}
        map_id_2_prod_hash = pkl.load(
            open('map_id_to_hash_products.dict', 'rb'))

        index_title_emb = AnnoyIndex(100)
        index_title_emb.load('./annoy')
        model = Word2Vec.load('./w2v_products.w2v_gensim')

        app.logger.info('Запрос' + text)

        listik = self.normalize_text(text).split(' ')

        vec = np.zeros(100)
        for i in listik:
            part_of_vec = None
            try:
                part_of_vec = model[i]
            except KeyError:
                pass
            if part_of_vec is not None:
                vec += part_of_vec

        annoy_res = list(
            index_title_emb.get_nns_by_vector(vec, 13, include_distances=True))

        app.logger.info('Соседи:')
        listik = []
        for annoy_id, annoy_sim in itertools.islice(zip(*annoy_res), 13):
            image_id = map_id_2_prod_hash[annoy_id]
            listik.append(image_id)
            app.logger.info(data_storage[image_id], 1 - annoy_sim ** 2 / 2)
        return self.data.ix[listik]

    def normalize_text(self, text):
        return creat_files_for_w2v_and_annoy.__normalize_text__(text)
