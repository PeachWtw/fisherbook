#encoding:utf-8
import json

from flask import request, jsonify, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.model.gift import Gift
from app.model.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo

from app.web import web
from app.forms.book import SearchForm
@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            # r = yushu_book.search_by_isbn(q)
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book,q)
    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html',books=books)
    # return jsonify(books.__dict__)
    # return json.dumps(books,default=lambda o: o.__dict__)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book =BookViewModel(yushu_book.first)
    has_in_gifts = False
    has_in_wishes = False
    if current_user.is_authenticated:
        if Gift.query.filter_by(isbn=isbn,uid=current_user.id,
                                     launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(isbn=isbn,uid=current_user.id,
                                     launched=False).first():
            has_in_wishes = True

    trade_gifts =Gift.query.filter_by(isbn=isbn,launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn,launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',book=book,wishes=trade_wishes_model,gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes,has_in_gifts=has_in_gifts)
