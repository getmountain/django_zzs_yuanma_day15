# 类和对象，基于类实例化对象。

# 类
class Foo:
    v1 = 123

    def __init__(self, name):
        self.name = name

    def func(self):
        pass


# 对象
obj1 = Foo("武沛齐")
obj2 = Foo("杨峰")
