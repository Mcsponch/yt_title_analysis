import pandas as pd
import numpy as np

import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams


def _load_dataframe(path):
    df = pd.read_csv(path)
    print('Data loaded from', path)
    print(df.head(3))
    return df


def _make_ngrams(n_engrams, df):
    print(f'Making a list of {n_engrams}grams')
    ngram_list = []
    for i in df['video_titles']:
        text_tokens = word_tokenize(i.lower())
        ngram_instance = list(ngrams(text_tokens, n_engrams))
        ngram_list.extend(ngram_instance)
    print('Done')
    return ngram_list


def _clean_punct_ngrams(n_ngrams, ngram_list):
    print(f'Removing {n_ngrams}grams with punctuation')
    idx = 0
    while idx < n_ngrams:
        ngram_list = [ngram for ngram in ngram_list if ngram[idx].isalpha()]
        print('Removing n_grams with punctuation in position', idx)
        idx += 1
    
    print('Done')
    return ngram_list


def _clean_stopwords_ngrams(n_ngrams, ngram_list):
    stopwords_spanish = stopwords.words('spanish')
    print(f'Removing {n_ngrams}grams with stopwords')
    idx = 0
    while idx < n_ngrams:
        ngram_list = [ngram for ngram in ngram_list if not ngram[0] in stopwords_spanish]
        print('Removing n_grams with stopword in position', idx)
        idx += 1
    
    print('Done')
    return ngram_list


def _make_fdist(ngram_list):
    print('Calculating distribution')
    fdist = FreqDist(ngram_list)
    print('Most common ngrams', fdist.most_common(5))
    return fdist


def _export_ngrams(n_ngrams, fdist ,type, source):
    df_ngrams = pd.DataFrame.from_dict(fdist, orient='index')
    df_ngrams.columns = ['frequency']
    df_ngrams.index.name = f'{type}_{n_ngrams}grams, '
    print(f'Saving as: {source}_{df_ngrams.index.name}_freq.csv')
    df_ngrams.to_csv(f'{source}_{df_ngrams.index.name}_freq.csv')




def run():
    df_path = input('Enter the path to the title database: ')
    df = _load_dataframe(df_path)
    source = str(df['source'][0])
    desired_ngrams = int(input('Size of n gram: '))
    ngram_list = _make_ngrams(desired_ngrams, df)

    no_punct_ngrams =_clean_punct_ngrams(desired_ngrams, ngram_list)
    no_punct_fdist =_make_fdist(no_punct_ngrams)
    _export_ngrams(desired_ngrams, no_punct_fdist, type='no_punct', source=source)

    clean_ngrams = _clean_stopwords_ngrams(desired_ngrams, no_punct_ngrams)
    clean_fdist = _make_fdist(clean_ngrams)
    _export_ngrams(desired_ngrams, clean_fdist, type='clean', source=source)

    print('Done')






if __name__ == '__main__':
    run()