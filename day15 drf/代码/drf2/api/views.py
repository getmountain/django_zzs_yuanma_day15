import datetime
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.request import Request
from api import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="get_gender_display")  # 只看这里
    title = serializers.CharField(source="depart.title")  # ["depart","depart"]
    order = serializers.IntegerField(source="order")

    class Meta:
        model = models.UserInfo
        fields = ["name", "age", "xx"]
        list_serializer_class = serializers.ListSerializer


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        # 1.获取数据
        queryset = models.UserInfo.objects.all()
        # 2.序列化
        ser = UserSerializer(instance=queryset, many=True)

        # 3.返回给用户
        context = {"status": True, "data": ser.data}

        return Response(context)


from django.core.validators import EmailValidator, RegexValidator
from rest_framework import exceptions


class DepartSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=20, min_length=6)
    order = serializers.IntegerField(required=False, max_value=100, min_value=10)
    level = serializers.ChoiceField(choices=[(1, "高级"), (2, "中级")])
    # email = serializers.EmailField()
    # email = serializers.CharField(validators=[EmailValidator(message="邮箱格式错误")])
    email = serializers.CharField(validators=[RegexValidator(r"\d+", message="邮箱格式错误"), ])

    def validate_email(self, value):
        if len(value) > 6:
            raise exceptions.ValidationError("字段钩子校验失败")
        return value

    def validate(self, attrs):
        print("validate=", attrs)
        # api_settings.NON_FIELD_ERRORS_KEY
        raise exceptions.ValidationError("全局钩子校验失败")  # non_field_errors
        # return attrs


class DepartModelSerializer(serializers.ModelSerializer):
    more = serializers.CharField(required=True)

    class Meta:
        model = models.Depart
        fields = ["title", "order", "more"]
        extra_kwargs = {
            "title": {"max_length": 5, "min_length": 1},
            "order": {"min_value": 5},
            # "count": {"validators": [RegexValidator(r"\d+", message="格式错误")]},
        }


class DepartView(APIView):

    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # print(request.data)

        # 2.校验
        ser = DepartModelSerializer(data=request.data)
        if ser.is_valid():
            print("视图", ser.validated_data)
            ser.validated_data.pop("more")
            ser.save(count=100)
        else:
            print("视图", ser.errors)

        # ser = DepartSerializer(data=request.data)
        # ser.is_valid(raise_exception=True)  # 成功，抛出异常 raise ValidationError(self.errors)
        # print(ser.validated_data)

        return Response("成功")


class UsModelSerializer(serializers.ModelSerializer):
    depart_id = serializers.IntegerField()
    tags = serializers.IntegerField()

    # mytag = serializers.DictField()

    class Meta:
        model = models.UserInfo
        fields = ["name", "age", "gender", "depart_id", "tags"]

    def validate_tags(self, value):
        print(value)
        # return value
        # return [999,990]
        queryset = models.Tag.objects.filter(id=value)
        return queryset


class UsView(APIView):
    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # print(request.data)

        # 2.校验
        ser = UsModelSerializer(data=request.data)
        if ser.is_valid():
            print("视图", ser.validated_data)
            # ser.validated_data.pop("tags")
            instance = ser.save()
            instance.id
            instance.name
            instance.age
        else:
            print("视图", ser.errors)
        return Response("成功")


class DpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = ["id", "title", "order", "count"]
        extra_kwargs = {
            "id": {"read_only": True},
            "count": {"write_only": True}
        }


class DpView(APIView):
    def post(self, request, *args, **kwargs):
        ser = DpModelSerializer(data=request.data)
        if ser.is_valid():
            instance = ser.save()
            print(instance)
            xx = DpModelSerializer(instance=instance)
            return Response(xx.data)

        else:
            return Response(ser.errors)


class P1ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = "__all__"


class MyCharField(serializers.CharField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'get_{field_name}'.format(field_name=field_name)
        super().bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)


class UusModelSerializer(serializers.ModelSerializer):
    v1 = serializers.CharField(source="depart.title", read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "age", "gender", "depart", "v1", "name"]
        extra_kwargs = {
            "id": {"read_only": True},
            "gender": {"write_only": True},
        }

    def get_name(self, obj):
        return 1111


class UusView(APIView):
    def post(self, request, *args, **kwargs):
        ser = UusModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)


class NbCharField(serializers.IntegerField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name  # None

        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'xget_{field_name}'.format(field_name=field_name)  # "get_gender"

        super().bind(field_name, parent)

    def get_attribute(self, instance):
        method = getattr(self.parent, self.method_name)
        return method(instance)

    def to_representation(self, value):
        return str(value)


class NbModelSerializer(serializers.ModelSerializer):
    gender = NbCharField()

    class Meta:
        model = models.NbUserInfo
        fields = ["id", "name", "age", 'gender']
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def xget_gender(self, obj):
        return obj.get_gender_display()


class NbView(APIView):
    def post(self, request, *args, **kwargs):

        # obj = models.NbUserInfo.objects.first()
        # print(obj.id, obj.get_gender_display(), obj.gender)

        ser = NbModelSerializer(data=request.data)
        if ser.is_valid():
            instance = ser.save()
            print(type(instance))
            print(instance.get_gender_display)
            print(instance.id, instance.get_gender_display(), instance.gender)
            return Response(ser.data)
        else:
            return Response(ser.errors)


from api.ext.hook import NbHookSerializer


class SbModelSerializer(NbHookSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.NbUserInfo
        fields = ["id", "name", "age", "gender"]
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def nb_gender(self, obj):
        return obj.get_gender_display()

    def nb_name(self, obj):
        return obj.get_gender_display()


class SbView(APIView):
    def post(self, request, *args, **kwargs):
        ser = SbModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)
