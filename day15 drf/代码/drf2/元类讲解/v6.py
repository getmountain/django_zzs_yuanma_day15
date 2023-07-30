class SerializerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        data_dict = {}
        for k, v in list(attrs.items()):  # {"v1":123,"v2":123,"v3":123}
            if isinstance(v, int):
                data_dict[k] = attrs.pop(k)
        attrs['_declared_fields'] = data_dict
        return super().__new__(cls, name, bases, attrs)


class BaseSerializer(object):
    pass


class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
    pass


class ModelSerializer(Serializer):
    pass


class UserSerializer(ModelSerializer):
    v1 = 123
    v2 = 456
    v3 = "哈哈哈"


print(UserSerializer.v3)
print(UserSerializer._declared_fields)
