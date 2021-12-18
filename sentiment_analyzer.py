import os

import nltk
import pandas as pd

# nltk.download(['names', 'stopwords', 'averaged_perceptron_tagger', 'vader_lexicon', 'punkt'])


def load_news_articles():
    news_sources = ['cnn', 'fox', 'reuters']
    search_terms = ['george floyd', 'black lives matter', 'all lives matter']
    df = pd.DataFrame()
    for each_source in news_sources:
        all_articles = pd.DataFrame()
        for each_term in search_terms:
            label_name = each_term.replace(' ', '-')
            file_name = f'scrappers/articles/{label_name}-posts-{each_source}.json'
            print("This is file name: ", file_name)
            _file = open(file_name, 'r')
            _term_source_df = pd.read_json(_file)
            _term_source_df['search_term'] = each_term
            print(_term_source_df.head())
            all_articles = all_articles.append(_term_source_df)
        all_articles['news_source'] = each_source
        df = df.append(all_articles)
    return df


df = load_news_articles()
print(df.head())

from nltk.sentiment import sentiment_analyzer