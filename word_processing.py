from nltk import text
from nltk.util import pr
import pandas as pd
import numpy as np

import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def _load_dataframe(path):
    df = pd.read_csv(path)
    print('Data loaded from', path)
    print(df.head(3))
    return df


def _get_text_from(df):
    print('Extracting video titles from data frame...')
    titles = df['video_titles'].to_list()
    spacer = ' '
    text = spacer.join(titles)
    print('Done')
    return text


def _tokenize(text):
    print('Geting tokens from text...')
    tokens = word_tokenize(text.lower())
    print('Done')
    return tokens


def _clean_tokens(tokens):
    print('Cleaning tokens...')
    stopwords_spanish = set(stopwords.words('spanish'))
    print('Removing punctuation...')
    tokens_no_punct = [token for token in tokens if token.isalpha()]
    print('Removing stopwords')
    tokens_clean = [token for token in tokens_no_punct if not token in stopwords_spanish]
    print('Done')
    return tokens_clean


def _make_dist(tokens):
    print('Making distribution')
    fdist = FreqDist(tokens)
    print('Done')
    print('Top 5 words', fdist.most_common(5))
    return fdist


def _export_freq_database(fdist, source):
    df_fdist = pd.DataFrame.from_dict(fdist, orient='index')
    df_fdist.columns = ['frequency']
    df_fdist.index.name = 'term'
    df_fdist.to_csv(f'{source}_word_freq.csv')
    print('Done')


def run():
    df_path = input('Enter the path to the title database: ')
    df = _load_dataframe(df_path)
    source = str(df['source'][0])
    titles_text = _get_text_from(df)
    text_tokens = _tokenize(titles_text)
    tokens_clean = _clean_tokens(text_tokens)
    fdist = _make_dist(tokens_clean)
    _export_freq_database(fdist)


if __name__ == '__main__':
    run()