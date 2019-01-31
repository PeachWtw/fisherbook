from flask import current_app
from sqlalchemy.orm import relationship

from app.model.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, desc, func


from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer,primary_key=True)
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    launched = Column(Boolean,default=False)
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer,ForeignKey('book.id'))

    def is_yourself_gift(self,uid):
        return True if self.uid == uid else False
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        return Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()

    @classmethod
    def get_user_gifts(cls,uid):
        return Gift.query.filter_by(
            uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.model.wish import Wish
        # all_data = Wish.query.filter_by(launched=False).group_by(Wish.isbn).all()
        count_list = db.session.query(func.count(Wish.id),Wish.isbn).filter(
            Wish.launched == False,Wish.isbn.in_(isbn_list),Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{"count": item[0], "isbn": item[1] } for item in count_list]
        return count_list

