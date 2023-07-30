# 创建类：方式1
# class Foo(object):
#     v1 = 123
#
#     def func(self):
#         return 999


# 创建类：方式2
# 类名 = type("类名", (父类,) , {成员} )
Foo = type("Foo", (object,), {"v1": 123, "func": lambda self: 999})

# obj = Foo()
# print(obj.v1)
# print(obj.func())
