from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import (
    Response,
)  # drf 的 Response对象是 Django 的HttpResponse的子类

from django.views import View
from django.http.response import JsonResponse
from rest_framework import status


class StudentView(View):
    def get(self, request):  # django提供的View视图，在视图方法中传入的request变量是 WSGIRequest
        print(
            f"request={request}"
        )  # WSGIRequest -->父类--> django.http.request.HttpRequest
        return JsonResponse({"msg": "ok"})


class StudentAPIView(APIView):
    def get(self, request):
        # rest_framework.request.Request 是属于 drf单独声明的请求处理对象，与Django 提供的HttpRequest不是同一个，甚至没有任何继承关系
        print(f"drf.request={request}")
        print(f"django.request={request._request}")  # WSGIRequest
        return Response({"msg": "ok"})

    def post(self, request):
        # 添加数据
        # 获取请求体数据，使用的是 request.data 类似 Django 中标准的 request.POST 和 request.FILES 属性
        print(f"request.data={request.data}")  # 接受的数据已经被 Parse 解析器转换成字典数据了！
        print(f"type :[request.data], {type(request.data)}")
        """
        1.客户端提交的是 json 数据
        request.data={'name': 'kobe'}
        type :[request.data], <class 'dict'>
        
        2. 客户端提交的表单数据
        request.data=<QueryDict: {'name': ['kobe']}>
        type :[request.data], <class 'django.http.request.QueryDict'>  
        """

        # 获取请求参数，使用的是 request.query_params 与 Django 标准的 request.GET 相同，只是更换了名字而已
        print(f"request.query_params={request.query_params}")
        print(f"type :[request.query_params], {type(request.query_params)}")
        """
        request.query_params=<QueryDict: {'info': ['NBA']}>
        type :[request.query_params], <class 'django.http.request.QueryDict'>
        """
        # 请求参数 info=NBA,CBA， 解析结果： NBA,CBA 类型为字符串
        print(request.query_params.get("info"), type(request.query_params.get("info")))
        # 请求参数 info=NBA,CBA， 解析结果： 【NBA,CBA】 类型为列表
        print(
            request.query_params.getlist("info"),
            type(request.query_params.getlist("info")),
        )

        return Response({"msg": "ok"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        # 更新数据
        return JsonResponse({"msg": "ok"})

    def patch(self, request):
        # 更新数据[部分]
        return JsonResponse({"msg": "ok"})

    def delete(self, request):
        # 删除数据
        return JsonResponse({"msg": "ok"})
