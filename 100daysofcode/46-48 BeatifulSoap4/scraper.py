import requests
import bs4


URL = 'https://www.gamespot.com/news/'

def pull_site():
    raw_site_page = requests.get(URL)
    raw_site_page.raise_for_status()
    return raw_site_page

def scrape(site):
    news_list = []
    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    html_news_list = soup.select('.card-item__content')


    for headers in html_news_list:
        news_list.append(headers.getText(separator=" "))


    for i in range(len(news_list)):
        print(news_list[i][7:-4])

if __name__ == '__main__':
    site = pull_site()
    scrape(site)
