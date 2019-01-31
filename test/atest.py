from flask import current_app, Flask

app =  Flask(__name__)

# ctx = app.app_context()
# ctx.push()
# a =  current_app
# debug = current_app.config['DEBUG']
# ctx.pop()

with app.app_context():
    a = current_app
    debug = current_app.config['DEBUG']

#实现了上下文协议的对象使用with
# 上下文管理器
# __enter__,__exit__
# 上下文表达式必须要返回一个上下文管理器
# with open(r"D:\t.txt") as f:
#     print(f.read())


# 注意with语句中as 后面的对象是enter方法中返回的对象

class MyResource:
    def __enter__(self):
        print('connect to resource')
        return self

    def excute(self):
        print('do something ')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('process exception')
        print('close the resource')
        return False # 不再向外抛出异常，如果是Fasle还会抛给外层
try:
    with MyResource() as obj_A:
        1/0
        obj_A.excute()
except Exception as e:
    print(e)


