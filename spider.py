from requests_html import HTMLSession


SITE_URL = 'https://itpanda.net'

session = HTMLSession()


class Spider:
    def get_category(self):
        data = []
        r = session.get(SITE_URL)
        nav = r.html.find('.nav', first=True)
        items = nav.find('.nav-item a')
        for item in items:
            cate = {
                'title': item.text,
                'link': f"{SITE_URL}{item.attrs['href']}"
            }
            data.append(cate)
        return data

    def get_books(self):
        category = self.get_category()
        for c in category:
            title = c['title']
            link = c['link']
            r = session.get(link)
            books_list = r.html.find('.list-unstyled', first=True)
            books = books_list.find('.media .mt-0 a')
            for book in books:
                bool_title, book_link = book.text, f"{SITE_URL}{book.attrs['href']}"
                # print(title, bool_title, book_link)
                r = session.get(book_link)
                pan = r.html.find('.text-danger')
                print(pan)


if __name__ == '__main__':
    s = Spider()
    s.get_books()
