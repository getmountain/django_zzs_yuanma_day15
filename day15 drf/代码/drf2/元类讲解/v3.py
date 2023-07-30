class MyType(type):

    def __new__(cls, *args, **kwargs):
        xx = super().__new__(cls, *args, **kwargs)
        return xx


Foo = MyType("Foo", (object,), {"v1": 123, "func": lambda self: 999})
