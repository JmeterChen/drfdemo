from django.views import View
import json
from .models import Student
from django.http.response import JsonResponse

# Create your views here.


"""
POST    /students/ 添加一个学生信息
GET     /students/  获取所有学生信息


GET     /students/<pk>/  获取所有学生信
PUT     /students/<pk>/  更新一个学生信息
DELETE  /students/<pk>/  删除一个学生信息

一个路由对应一个视图类，所以我们可以把5个API 分成2个类来完成
"""


class StudentView(View):
    """学生视图"""

    def post(self, request):
        """添加一个学生信息"""
        # 1. 接收客户单提交的数据
        req_data = json.loads(request.body)
        name = req_data.get("name")
        sex = req_data.get("sex")
        age = req_data.get("age")
        classmate = req_data.get("classmate")
        description = req_data.get("description")
        # 1.1 验证客户端的数据
        # 2. 操作数据库，保存数据
        instance = Student.objects.create(
            name=name,
            sex=sex,
            age=age,
            classmate=classmate,
            description=description
        )
        # 3.返回结果
        return JsonResponse(data={
            "name": instance.name,
            "sex": instance.sex,
            "age": instance.age,
            "classmate": instance.classmate,
            "description": instance.description,
            "id": instance.pk,
        }, status=201)

    def get(self, request):
        stu_list = list(Student.objects.values())
        return JsonResponse(data=stu_list, safe=False)


class StudentInfoView(View):
    def get(self, request, pk):
        """获取指定学生信息"""
        try:
            instance = Student.objects.get(pk=pk)
            return JsonResponse(data={
                "name": instance.name,
                "sex": instance.sex,
                "age": instance.age,
                "classmate": instance.classmate,
                "description": instance.description,
                "id": instance.pk,
            })
        except Student.DoesNotExist:
            return JsonResponse(data=None, status=201, safe=False)

    def put(self, request, pk):
        """更新一个学生的信息 """
        # 1. 接收客户单提交的数据
        req_data = json.loads(request.body)
        name = req_data.get("name")
        sex = req_data.get("sex")
        age = req_data.get("age")
        classmate = req_data.get("classmate")
        description = req_data.get("description")
        # 1.1 验证客户端的数据
        # 2. 操作数据库，保存数据
        try:
            instance = Student.objects.get(pk=pk)
            instance.name = name
            instance.sex = sex
            instance.age = age
            instance.classmate = classmate
            instance.description = description
            instance.save()
            return JsonResponse(data={
                "name": instance.name,
                "sex": instance.sex,
                "age": instance.age,
                "classmate": instance.classmate,
                "description": instance.description,
                "id": instance.pk,
            })
        except Student.DoesNotExist:
            return JsonResponse(data=None, status=201, safe=False)

    def delete(self, request, pk):
        try:
            Student.objects.filter(pk=pk).delete()
        except:
            pass
        return JsonResponse(data=None, status=201, safe=False)
