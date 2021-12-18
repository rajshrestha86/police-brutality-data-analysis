import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from cnn_api import search_terms
driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.set_window_size(19800,1080)
# driver.set_page_load_timeout(30)

# click next page
total_articles_present = {}
for each in search_terms:
    counter = 0
    file_name = each.replace(' ', '-')
    articles = []
    with open(f'articles/{file_name}-url-cnn.json', 'r') as file:
        content = json.load(file)
        total_articles = len(content)
        for each_article in content:
            print(each_article)
            try:
                driver.get(each_article['url'])
                driver.execute_script("window.scrollTo(0, 2500)");
                driver.execute_script("window.scrollTo(2500, 5000)");
            except TimeoutException:
                print("#####################")
                print("Timeout..........")
                print("#####################")
                continue
            try:
                article = driver.find_element_by_css_selector('.zn-body-text')
            except NoSuchElementException:
                print("Not found: ", each_article['headline'])
                continue
            counter += 1
            article = article.text
            articles.append({
                'url': each_article['url'],
                'headline': each_article['headline'],
                'published_date': each_article['published_date'],
                'text': article
            })
            print("Article pulled: ", counter, total_articles, each, each_article['headline'])

    total_articles_present[each] = counter
    filename = f'articles/{file_name}-posts-cnn.json'
    with open(filename, 'w') as file:
        json.dump(articles, file)

print("Total articles of interest: ", total_articles_present)
driver.close()
