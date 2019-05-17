import pandas as pd
import sqlalchemy
import numpy as np

DB_CONFIG = {
    'username': 'bibliophagist',
    'password': '5264552',
    'host': 'localhost:3306',
    'dbname': 'article_seeker',
}

config = f"mysql://" \
    f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8"
engine = sqlalchemy.create_engine(config)

data = pd.read_csv('scopus.csv')
columns = ['Авторы', 'Название', 'Ссылка',
           'Краткое описание', 'Ключевые слова автора']
columns_new = ['authors', 'title', 'ref',
               'annotation', 'key_words']
delete_columns = [column not in columns for column in data.columns]
data = data.drop(columns=data.columns[delete_columns])
data = data.fillna(" ")

data.columns = columns_new

print(len(np.unique(data.index)), len(data.index))
data.to_sql('articles', con=engine, index=False, if_exists='append')
