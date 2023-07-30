class MyType(type):
    def __new__(cls, name, bases, attrs):
        # print(name, bases, attrs)
        del attrs['v1']
        attrs['dex'] = "xxxx"
        xx = super().__new__(cls, name, bases, attrs)
        return xx


# Foo = MyType("Foo", (object,), {"v1": 123, "func": lambda self: 999})
class Foo(object, metaclass=MyType):
    v1 = 123

    def func(self):
        pass


print(Foo.func)
print(Foo.dex)
