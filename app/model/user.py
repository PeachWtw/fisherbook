from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash,check_password_hash

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.model.base import Base, db
from app.model.drift import Drift
from app.model.gift import Gift
from app.model.wish import Wish
from app.spider.yushu_book import YuShuBook
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin,Base):
    id = Column(Integer,primary_key=True)
    nickname = Column(String(24),nullable=True)
    phone_number = Column(String(18),unique=True)
    _password = Column('pw',String(128),nullable=True)
    email = Column(String(50),unique=True,nullable=True)
    confirmed = Column(Boolean,default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer,default=0)
    receive_counter = Column(Integer,default=0)

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter) + '/' + str(self.receive_counter)
        )

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gift_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id,_pending=PendingStatus.Success).count()
        return True if floor(success_gift_count) - \
                       floor(success_receive_count/2) >=0 else False




    @property
    def password(self):
        return self._password


    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return check_password_hash(self.password,raw)

    def can_save_to_list(self,isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        #要求保存的书籍既不在赠送清单，也不在心愿清单
        gifting = Gift.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self,expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        temp = s.dumps({'id':self.id}).decode('utf-8')
        return temp

    @staticmethod
    def reset_password(new_password,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        id = data.get('id')
        with db.auto_commit():
            user = User.query.filter_by(id=id)
            user.password = new_password
        return True

"""你必须提供一个 user_loader 回调。这个回调用于从会话中存储的用户 ID 重新加载用户对象。
它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。比如:"""
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
