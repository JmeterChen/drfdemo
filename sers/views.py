from django.shortcuts import render

# Create your views here.


import json
from django.views import View
from sers.models import TbUser
from sers.mySerializers import User1Serializers, User2Serializers
from django.http.response import JsonResponse


class UsersView(View):

    def get(self, request):
        """序列化-序列化阶段的调用"""
        # 1.获取模型对象数据
        users = TbUser.objects.first()
        # 2. 实例化序列化器，得到序列化对象
        serializer = User1Serializers(instance=users)

        # 3. 调用序列化对象的data 属性方法获取转换后的数据
        data = serializer.data

        # 4. 响应数据
        return JsonResponse(data=data, safe=False)

    # def post0(self, request):
    #     """序列化-序列化阶段的调用"""
    #     # 1.获取模型对象数据
    #     users_list = TbUser.objects.all()
    #     # 2. 实例化序列化器，得到序列化对象
    #     serializer = User1Serializers(instance=users_list, many=True)
    #
    #     # 3. 调用序列化对象的data 属性方法获取转换后的数据
    #     data = serializer.data
    #
    #     # 4. 响应数据
    #     return JsonResponse(data=data, safe=False)

    def post(self, request):
        """序列化-序列化阶段的调用"""

        req = json.loads(request.body)

        # 1. 实例化序列化器，得到序列化对象
        serializer = User2Serializers(data=req)

        # 1.2 调用序列化器进行数据校验
        # 1.2.1 这里直接使用 序列化器中的字段校验
        ret = serializer.is_valid()  # 服务端不抛出异常
        # ret = serializer.is_valid(raise_exception=True)        # 服务端直接抛出异常，代码不会继续往下执行
        print(f"ret:{ret}")

        # 1.3 获取验证以后的结果 并返回
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))

    def put(self, request):
        req = json.loads(request.body)
        print("req:", req)

        user_id = req.get("employee_id")
        user = TbUser.objects.filter(employee_id=user_id, is_delete=0).first()
        # 1. 实例化序列化器，得到序列化对象
        serializer = User2Serializers(data=req, instance=user, partial=True)

        ret = serializer.is_valid()  # 服务端不抛出异常
        # ret = serializer.is_valid(raise_exception=True)        # 服务端直接抛出异常，代码不会继续往下执行
        print(f"ret:{ret}")

        if ret:
            serializer.save()
            return JsonResponse(serializer.data, safe=True)
        else:
            return JsonResponse(dict(serializer.errors))
