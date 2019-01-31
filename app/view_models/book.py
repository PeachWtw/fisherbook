class BookViewModel:
    def __init__(self,book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages']
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property  #把一个方法变成属性调用的,可以让调用者写出简短的代码，同时保证对参数进行必要的检查
    def intro(self):
        intro = filter(lambda o: True if o else False,[self.author,self.publisher,self.price])
        return '/'.join(intro)

class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


