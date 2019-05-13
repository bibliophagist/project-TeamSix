from application import app
from application.machine import creat_files_for_w2v_and_annoy
import pickle as pkl
from annoy import AnnoyIndex
import itertools


class Seeker:
    def __init__(self):
        self.data = creat_files_for_w2v_and_annoy.creat()

    def find_article_by_id(self, _id):
        data_storage = {i[0]: i[1]['Название'] + ' ' + i[1]['Краткое описание']
                        for i in self.data.iterrows()}
        map_id_2_prod_hash = pkl.load(
            open('map_id_to_hash_products.dict', 'rb'))

        index_title_emb = AnnoyIndex(100)
        index_title_emb.load('./annoy')

        app.logger.info('Запрос' + str(data_storage[map_id_2_prod_hash[_id]]))

        annoy_res = list(
            index_title_emb.get_nns_by_item(_id, 13, include_distances=True))

        app.logger.info('Соседи:')

        for annoy_id, annoy_sim in itertools.islice(zip(*annoy_res), 13):
            image_id = map_id_2_prod_hash[annoy_id]
            app.logger.info(data_storage[image_id], 1 - annoy_sim ** 2 / 2)
