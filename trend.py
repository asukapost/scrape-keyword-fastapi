from pytrends.request import TrendReq
import pandas as pd
from pytrends.request import TrendReq

def get_trend_keywords(query_param=None):
    pytrend = TrendReq(hl='ja-jp', tz=540)

    # Related Keywords
    if query_param:
        kwds = query_param
    else:
        kwds = ["行政書士", "家族信託", "遺言"]
    pytrend.build_payload(kw_list=kwds, timeframe='now 7-d', geo='JP')
    related_queries = pytrend.related_queries()


    results = []
    for key in related_queries:
        df_rising = related_queries[key]['rising'].sort_values(by='value', ascending=False)
        rising_keywords = [word for word in df_rising['query'][:5]]
        for kwd in rising_keywords:
            results.append(kwd)
    # Get Japan Trend
    pytrend = TrendReq(hl='ja-jp', tz=540)
    df = pytrend.trending_searches(pn='japan')
    df.head(20)

    for kwd in df[df.columns[0]][:5]:
        results.append(kwd)

    df = pd.DataFrame({'Keyword': results}).drop_duplicates()

    return df

if __name__ == "__main__":
    get_trend_keywords()