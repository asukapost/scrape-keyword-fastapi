import pandas as pd
import numpy as np
from trend import get_trend_keywords
from scrape import scrape_to_df
import spacy

def cosine_similarity(a, b):
    return a.dot(b)/np.sqrt(a.dot(a) * b.dot(b))


def nlp_process(query_param):
    keywrods_df = get_trend_keywords(query_param)
    kwds = []
    for kwd in keywrods_df["Keyword"]:
        items = kwd.split()
        for item in items:
            kwds.append(item)
    kwds_df = pd.DataFrame({'Keyword': kwds})
    kwds_df = kwds_df.drop_duplicates()

    kwds_text = ""
    for kwd in kwds_df['Keyword']:
        kwds_text += kwd
    kwds_text += "家族信託遺言書作成"

    print('-'*40, "Keywords", '-'*40)
    print(kwds_text)
    nlp = spacy.load("ja_core_news_sm")
    scores = []
    kwds_vec = nlp(kwds_text).vector

    news_df = scrape_to_df(query_param)
    for text in news_df['Content']:
        content_vec = nlp(text).vector
        score = cosine_similarity(kwds_vec, content_vec)
        scores.append(score)
    
    news_df['Score'] = scores
    news_df = news_df.sort_values(by='Score', ascending=False)

    return_item = {
        'Keywords': kwds_text,
        'Urls': news_df['Url'][:10].values.tolist(),
        'Contents': news_df['Content'][:10].apply(lambda x: x[:250] if len(x) > 250 else x).values.tolist()
    }

    return return_item



    