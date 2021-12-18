import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from cnn_api import search_terms

driver = webdriver.Chrome('/usr/bin/chromedriver')

# click next page
total_articles_present = {}
for each in search_terms:
    counter = 0
    articles = []
    file_name = each.replace(' ', '-')
    with open(f'articles/{file_name}-url-reuters.json', 'r') as file:
        content = json.load(file)
        total_articles = len(content)
        for each_article in content:
            driver.get(f'https://www.reuters.com{each_article["url"]}')
            try:
                article = driver.find_element_by_css_selector('.ArticleBodyWrapper')
            except NoSuchElementException:
                print("Not found: ", each_article['headline'])
                continue
            article = article.text
            articles.append({
                'url': each_article['url'],
                'headline': each_article['headline'],
                'published_date': each_article['published_date'],
                'text': article
            })
            counter += 1
            print("Article pulled: ", counter, total_articles, each, each_article['headline'])
    total_articles_present[each] = counter
    filename = f'articles/{file_name}-posts-reuters.json'
    with open(filename, 'w') as file:
        json.dump(articles, file)
print("Total articles of interest: ", total_articles_present)
driver.close()
