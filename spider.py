import os
from requests_html import HTMLSession
from requests.adapters import HTTPAdapter


SITE_URL = 'https://itpanda.net'

session = HTMLSession()
session.mount(SITE_URL, HTTPAdapter(max_retries=5))

PROXIES_SERVER = os.environ.get('PROXIES_SERVER')
PROXIES = {'http': PROXIES_SERVER, 'https': PROXIES_SERVER}


class Spider:
    def get_category(self):
        data = []
        r = session.get(SITE_URL, proxies=PROXIES)
        nav = r.html.find('.nav', first=True)
        items = nav.find('.nav-item a')
        for item in items:
            title, num = item.text.split(' ')
            cate = {
                'title': title,
                'num': num.lstrip('(').rstrip(')'),
                'link': f"{SITE_URL}{item.attrs['href']}"
            }
            data.append(cate)
        return data

    def get_books(self):
        category = self.get_category()
        for c in category:
            title = c['title']
            link = c['link']
            num = int(c['num'])

            book_num = 0
            page = 1
            while book_num < num:
                r = session.get(f'{link}?sort_by=created_at&page={page}', proxies=PROXIES)
                books_list = r.html.find('.list-unstyled', first=True)
                books = books_list.find('.media .mt-0 a')

                for book in books:
                    book_num += 1
                    bool_title, book_link = book.text, f"{SITE_URL}{book.attrs['href']}"
                    try:
                        pan_url, pan_key = self.get_book(book_link)
                        print(f'{title}, {bool_title}, {pan_url}, {pan_key}')
                    except Exception as e:
                        print(e, bool_title, book_link)
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
    s.get_books()
