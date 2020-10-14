import requests
from bs4 import BeautifulSoup as BS
import json

class Parser(object):

    def start_parse(self):
        # необходимо получить максимальное число страниц
        request = requests.get('https://xakep.ru/page/1/?s=python')
        soup = BS(request.text, 'html.parser')
        pages = soup.find('span', {'class': 'pages'}).text[-2:]

        # перебор каждой страницы
        for page in range(1, int(pages)+1):
            request = requests.get(f'https://xakep.ru/page/{page}/?s=python')
            soup = BS(request.text, 'html.parser')
            all_articles = soup.find_all('div', {'class': 'block-article bd-col-md-6 bdaiaFadeIn'})

            # перебор каждой статьи
            for article in all_articles:
                title = article.find('h3', {'class': 'name entry-title'}).find('span').text
                link =  article.find('h3', {'class': 'name entry-title'}).find('a')['href']
                date =  article.find('span', {'class': 'bdayh-date'}).text
                views = article.find('div', {'class': 'bdaia-post-view'}).text
                written_article = {
                    'title': title,
                    'link': link,
                    'date': date,
                    'views': views
                }
                # запись данных
                with open('articles.json', 'a', encoding='utf8') as json_file:
                    json.dump(written_article, json_file, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    parser = Parser()
    parser.start_parse()
