
from sqlalchemy import String, Column, Integer, Boolean, ForeignKey, SmallInteger, desc, func
from sqlalchemy.orm import relationship

from app.model.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer,primary_key=True)
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean,default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls,uid):
        return  Wish.query.filter_by(
            launched=False,uid=uid).order_by(
            desc(Wish.create_time)).all()

    @classmethod
    def get_gift_counts(cls,isbn_list):
        from app.model.gift import Gift
        count_list = db.session.query(func.count(Gift.id),Gift.isbn).filter(
            Gift.launched==False,Gift.isbn.in_(isbn_list),Gift.status==1).group_by(Gift.isbn).all()
        count_list = [{"count":w[0],"isbn":w[1]} for w in count_list]
        return count_list