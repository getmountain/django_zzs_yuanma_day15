class MyType(type):
    def __new__(cls, name, bases, attrs):
        print(name, bases, attrs)
        xx = super().__new__(cls, name, bases, attrs)
        return xx

    def __call__(cls, *args, **kwargs):
        print("执行type的call")
        obj = cls.__new__(cls, *args, **kwargs)
        print("----")
        cls.__init__(obj, *args, **kwargs)
        return obj


class Base(object, metaclass=MyType):
    def __init__(self):
        print("初始化")

    def __new__(cls, *args, **kwargs):
        print("实例化类的对象")
        return object.__new__(cls)

    def __call__(self, *args, **kwargs):
        print("Base.call")


# 1.类是有MyType创建出来。   类其实是MyType类实例化的对象。
# 2.Base是类，MyType类的对象；  Base()    MyType()()    -> 类实例化出来的对象    对象()
obj = Base()
obj()
