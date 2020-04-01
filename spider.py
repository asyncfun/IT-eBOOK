import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests.adapters import HTTPAdapter


SITE_URL = 'https://itpanda.net'

session = HTMLSession()
session.mount(SITE_URL, HTTPAdapter(max_retries=5))

PROXIES_SERVER = os.environ.get('PROXIES_SERVER')
PROXIES = {'http': PROXIES_SERVER, 'https': PROXIES_SERVER}


class Spider:
    def get_markdown(self):
        r = session.get(SITE_URL, proxies=PROXIES)

        nav = r.html.find('ul.nav', first=True)
        soup = BeautifulSoup(nav.html, features="lxml")
        ul = soup.find('ul')
        items = ul.find_all('li', recursive=False)
        print('# IT eBOOK')
        for item in items:
            sub_items = item.ul.find_all('li')
            cate_title = item.a.string.split('(')[0].strip()
            cate_link = f'{SITE_URL}{item.a["href"]}'
            print(f'## {cate_title}')
            for sub in sub_items:
                sub_cate_title = sub.a.string.split('(')[0].strip()
                num = int(sub.a.string.split('(')[1].strip(')').strip())
                sub_cate_link = f'{SITE_URL}{sub.a["href"]}'
                print(f'### {sub_cate_title}')
                self.get_books_by_cate(cate_link=sub_cate_link, num=num)
            if not sub_items:
                num = int(item.a.string.split('(')[1].strip(')').strip())
                self.get_books_by_cate(cate_link=cate_link, num=num)

    def get_books_by_cate(self, cate_link, num):
        book_num = 0
        page = 1
        while book_num < num:
            r = session.get(f'{cate_link}?sort_by=created_at&page={page}', proxies=PROXIES)
            books_list = r.html.find('.list-unstyled', first=True)
            books = books_list.find('.media .mt-0 a')

            for book in books:
                book_num += 1
                bool_title, book_link = book.text, f"{SITE_URL}{book.attrs['href']}"
                pan_url, pan_key = self.get_book(book_link)
                print(f'- [{bool_title}]({pan_url}) 提取码: {pan_key}')
            page += 1

    def get_book(self, book_link):
        r = session.get(book_link, proxies=PROXIES)
        downloads = r.html.find('.text-danger.mr-2')
        download = downloads[1] if len(downloads) > 1 else downloads[0]
        download_url = f"{SITE_URL}{download.attrs['href']}"
        r = session.get(download_url, proxies=PROXIES)

        pans = r.html.find('.text-danger')
        pan = pans[1] if len(pans) > 1 else pans[0]
        pan_url = pan.attrs['href']
        pan_key = r.html.search('提取码:{}</p>')[0]
        return pan_url, pan_key


if __name__ == '__main__':
    s = Spider()
    s.get_markdown()
