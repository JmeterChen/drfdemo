from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication, SessionAuthentication


# Create your views here.


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        print(request.user)
        print(dir(request.user))
        return Response({"msg": "ok"})


from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ExampleInfoView(APIView):
    pass


"""
过滤Filtering
对于列表数据可能需要根据字段进行过滤，我们可以通过添加 django-filter扩展来增强支持
pip install django-filter
"""

from rest_framework.viewsets import ModelViewSet

from stuapi.models import Student
from students.mySerializers import StudentModelSerializers

# 针对 app  局部进行配置
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status


class OptModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["sex", "classmate"]


from rest_framework.views import APIView


class OptAPIView(APIView):
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["sex", "classmate"]

    def get(self, request):
        # 1.获取数据库中内容
        db_data = Student.objects.all()

        # 2. 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializers(instance=db_data, many=True)

        # 3. 序列化从数据库中得到的内容并返回给客户端
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import GenericAPIView


class OptGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["sex", "classmate"]

    def get(self, request):
        # 1. 从数据库中读取学生列表信息
        instance = self.get_queryset()  # GenericAPIView提供的 get_queryset
        # 2. 序列化
        serializer = self.get_serializer(instance=instance, many=True)

        # 3.转换数据并返回给客户端
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin


class OptMixinAPIView(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers

    def get(self, request):
        return self.list(request)
