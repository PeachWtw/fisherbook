from flask import render_template

from app.model.gift import Gift
from app.view_models.book import BookViewModel
from . import web


__author__ = '七月'


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    recent = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html',recent=recent)


@web.route('/personal')
def personal_center():
    pass
