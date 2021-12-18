import json
import re
from datetime import datetime
from selenium import webdriver

driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.set_page_load_timeout(30)

from bs4 import BeautifulSoup
import requests
driver.get('https://www.reuters.com/search/news?sortBy=relevance&dateRange=all&blob=george+floyd')

api_url = 'https://www.reuters.com/assets/searchArticleLoadMoreJson?' \
          'blob={query}&bigOrSmall=big&articleWithBlog=true&sortBy=date&dateRange=pastYear&numResultsToShow=50&pn={page}&callback=addMoreNewsResults'
search_url = 'https://www.reuters.com/search/news?sortBy=date&dateRange=pastYear&blob={query}'
# api_url = 'https://api.foxnews.com/search/web?q={query}+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section+more:pagemap:metatags-pagetype:' \
# 'article+more:pagemap:metatags-dc.type:Text.Article&siteSearch=foxnews.com&siteSearchFilter=i&sort=date:r:20200525:20200731'
search_terms = ['george floyd', 'black lives matter', 'all lives matter']
# search_terms = ['all lives matter']
date_from = datetime.strptime('2020-05-25', '%Y-%m-%d').date()
date_to = datetime.strptime('2020-07-31', '%Y-%m-%d').date()

def cleanhtml(raw_html):
  return raw_html
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_json(resp):
    resp_text = resp.text
    # print(resp_text)
    regex = 'addMoreNewsResults\((?P<res>\s+(.|\n)*?)\);'
    print(resp.status_code, resp_text)
    match = re.search(regex, resp_text).groupdict()

    items = f'{match["res"]}'
    items = cleanhtml(items)
    json_obj = driver.execute_script(f'return {items}')
    return {
        'items': json_obj['news']
    }


if __name__ == '__main__':
    for each in search_terms:
        news_articles = []
        search_query = each.replace(' ', '+')
        resp = requests.get(search_url.format(query=search_query))
        soup = BeautifulSoup(resp.text, "html.parser")
        total = int(soup.find('span', {'class': 'search-result-count-num'}).text.replace(',', ''))
        news_url = search_url.format(query=search_query)

        total_res = total
        start = 1
        while start * 50 < total_res:
            url = api_url.format(query=search_query, page=start)
            response = requests.get(url)
            print("Url: ", url)
            if response.status_code == 400:
                break
            res = get_json(response)
            articles = res['items']
            for each_article in articles:
                print(each_article)
                url = each_article['href']
                headline = each_article['headline']
                try:
                    published_date = datetime.strptime(each_article['date'].split('2020')[0]+' 2020', '%B %d, %Y').date()
                except ValueError:
                    print("Date conversion error..... : ", each_article['date'])
                    continue
                if date_from <= published_date <= date_to:
                    news_articles.append({
                        'published_date': str(published_date),
                        'url': url,
                        'headline': headline
                    })
            print("Articles pulled: ", len(articles), "Cursor: ", start*50, total_res)
            start += 1
        print(f"Total articles pulled for: {each} - ", total_res, ", Of Interest: ", len(news_articles))
        file_name = each.replace(' ', '-')
        with open(f'articles/{file_name}-url-reuters.json', 'w') as file:
            json.dump(news_articles, file)
driver.close()
