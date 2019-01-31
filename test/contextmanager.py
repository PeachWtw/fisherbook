from contextlib import contextmanager

class MyResource():
    def query(self):
        print('get something')


@contextmanager
def my_func():
    print('start the connection')
    yield MyResource()
    print('end the connection')


with my_func() as r:
    r.query()