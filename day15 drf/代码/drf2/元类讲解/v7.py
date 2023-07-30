class Foo(object):
    pass

type
obj = Foo()
v1 = obj.__str__()  # <__main__.Foo object at 0x7fc2801c3850>
print(v1)
