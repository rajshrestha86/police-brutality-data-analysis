import json
import re
from datetime import datetime

import requests

api_url = 'https://api.foxnews.com/search/web?q={query}+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section+more:pagemap:metatags-pagetype:' \
'article+more:pagemap:metatags-dc.type:Text.Article&siteSearch=foxnews.com&siteSearchFilter=i&sort=date:r:20200525:20200731'
search_terms = ['george floyd', 'black lives matter', 'all lives matter']
date_from = datetime.strptime('2020-05-25', '%Y-%m-%d').date()
date_to = datetime.strptime('2020-07-31', '%Y-%m-%d').date()

def get_json(resp):
    resp_text = resp.text
    regex = '\"items\": \[(?P<items>(.|\n)*)\]'
    query_regex = '\"queries\": (?P<queries>\{(.|\n)*?\}),'
    s_query = re.search(query_regex, resp_text).groupdict()['queries']
    match = re.search(regex, resp_text).groupdict()
    items = f'[{match["items"]}]'
    items = json.loads(items)
    s_query = json.loads(s_query)
    return {
        'items': items,
        'meta': s_query
    }


if __name__ == '__main__':
    for each in search_terms:
        news_articles = []
        search_query = each.replace(' ', '%20')
        news_url = api_url.format(query=search_query)
        response = requests.get(news_url)
        res = get_json(response)
        meta = res['meta']
        print(meta['nextPage'])
        total_res = int(meta['nextPage'][0]['totalResults'])
        start = 0
        while start < total_res:
            url = f'{news_url}&start={start}'
            response = requests.get(url)
            print("Url: ", url)
            if response.status_code == 400:
                break
            res = get_json(response)
            articles = res['items']
            for each_article in articles:
                url = each_article['link']
                headline = each_article['pagemap']['metatags'][0]['twitter:title']
                for k, v in each_article.items():
                    print(k, v)
                print("Here madam: ", each_article['snippet'].rsplit('...')[0])
                try:
                    published_date = datetime.strptime(each_article['snippet'].split('...')[0], '%b %d, %Y ').date()
                except ValueError:
                    continue
                news_articles.append({
                    'published_date': str(published_date),
                    'url': url,
                    'headline': headline
                })
            print("Articles pulled: ", len(articles), "Cursor: ", start)
            start += 10
        print(f"Total articles pulled for: {each} - ", total_res, ", Of Interest: ", len(news_articles))
        file_name = each.replace(' ', '-')
        with open(f'articles/{file_name}-url-fox.json', 'w') as file:
            json.dump(news_articles, file)
