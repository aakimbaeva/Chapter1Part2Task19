from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime


def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('ul', class_='pagn').find_all('a')[-1].get('href')
    total_pages = pages.split('=')[-1]

    return int(total_pages)


def write_csv(data):
    with open('mobiles_database.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['price'], data['photo_link']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_="mr-3").find_all('article', class_="listing-item")

    for ad in ads:
        try:
            title = ad.find('div', class_='listing-item-main').find('a', class_='item listing-item-title').text.strip()
        except:
            title = ''

        try:
            price = ad.find('div', class_='listing-item-main').find('p', class_='listing-item-title').text.strip()
            total_price = price.split('\xa0')
        except:
            price = ''

        try:
            photo_link = ad.find('div', class_='listing-item-img-wrap').find('img').get('src')
        except:
            photo_link = ''

        data = {'title': title, 'price': price, 'photo_link': photo_link}

        write_csv(data)


def main():
    start = datetime.now()
    base_url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnyetelefony'
    url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnyetelefony'
    page_part = '?page='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = base_url + page_part +str(i)
        print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)
    end = datetime.now()
    work_time = end - start
    print(work_time)


if __name__ == '__main__':
    main()
