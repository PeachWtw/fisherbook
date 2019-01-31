from flask import current_app

from app.libs.httpmodule import HttpModule

class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    @property
    def first(self):
        return self.books[0]

    def __fill_single(self,book):
        self.total = 1
        self.books.append(book)

    def __fill_collections(self,books):
        self.total = books['total']
        self.books = [book for book in books['books']]

    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn)
        r = HttpModule.get(url)
        self.__fill_single(r)

    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,current_app.config['PER_PAGE'],page)
        r = HttpModule.get(url)
        self.__fill_collections(r)

    def caculate_start(self,page):
        return (page-1)*current_app.config['PER_PAGE']