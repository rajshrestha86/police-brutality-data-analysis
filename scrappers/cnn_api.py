from datetime import datetime

import json
import requests

api_url = 'https://search.api.cnn.io/content?size=50&q={query}&type=article&sort=relevance&category=us'
search_terms = ['george floyd', 'black lives matter', 'all lives matter']
date_from = datetime.strptime('2020-05-25', '%Y-%m-%d').date()
date_to = datetime.strptime('2020-07-31', '%Y-%m-%d').date()
if __name__ == '__main__':
    for each in search_terms:
        news_articles = []
        search_query = each.replace(' ', '%20')
        news_url = api_url.format(query=search_query)
        response = requests.get(news_url)
        res = response.json()
        meta = res['meta']
        total_res = meta['of']
        start = 0
        while start < total_res:
            url = f'{news_url}&from={start}'
            response = requests.get(url)
            res = response.json()
            articles = res['result']
            for each_article in articles:
                published_date = each_article['firstPublishDate'].split('T')[0]  # '2020-05-27T18:45:56Z'
                url = each_article['url']
                headline = each_article['headline']
                _published = datetime.strptime(published_date, '%Y-%m-%d').date()
                if date_from <= _published <= date_to:
                    news_articles.append({
                        'published_date': published_date,
                        'url': url,
                        'headline': headline
                    })
            print("Articles pulled: ", len(articles), "Cursor: ", start)
            start += 50
        print(f"Total articles pulled for: {each} - ", total_res, ", Of Interest: ", len(news_articles))
        file_name = each.replace(' ', '-')
        with open(f'articles/{file_name}-url-cnn.json', 'w') as file:
            json.dump(news_articles, file)
