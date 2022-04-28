# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-07


from django.urls import path, re_path, include

# v1
from .views import StudentAPIView, StudentInfoAPIView

# v2
from .views import StudentGenericAPIView, StudentInfoGenericAPIView

# v3
from .views import StudentMixinAPIView, StudentInfoMixinAPIView

# v4
from .views import StudentView, StudentInfoView

# v5
from .views import StudentSimpleView, StudentSimpleInfoView

# v6
from .views import StudentViewSet

# v7
from .views import StudentGenericViewSet

# v8
from .views import StudentMixinViewSet

# v9
from .views import StudentReadOnlyViewSet

# v10
from .views import StudentModelViewSet

student_v1 = [
    path("students/", StudentAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoAPIView.as_view()),
]

student_v2 = [
    path("students/", StudentGenericAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoGenericAPIView.as_view()),
]

student_v3 = [
    path("students/", StudentMixinAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoMixinAPIView.as_view()),
]

# 视图子类1
student_v4 = [
    path("students/", StudentView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoView.as_view()),
]

# 视图子类2
student_v5 = [
    path("students/", StudentSimpleView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentSimpleInfoView.as_view()),
]

# ViewSet 普通视图集
student_v6 = [
    path("students/", StudentViewSet.as_view({"get": "get_list", "post": "post"})),
    re_path(
        "^students/(?P<pk>\d+)/$",
        StudentViewSet.as_view(
            {"put": "put", "get": "get_student_info", "delete": "delete"}
        ),
    ),
]

# GenericViewSet 通用视图集
student_v7 = [
    path("students/", StudentGenericViewSet.as_view({"get": "list", "post": "create"})),
    re_path(
        "^students/(?P<pk>\d+)/$",
        StudentGenericViewSet.as_view(
            {"put": "update", "get": "retrieve", "delete": "destroy"}
        ),
    ),
]

# GenericViewSet + Mixin 混合视图集
student_v8 = [
    path("students/", StudentMixinViewSet.as_view({"get": "list", "post": "create"})),
    re_path(
        "^students/(?P<pk>\d+)/$",
        StudentMixinViewSet.as_view(
            {"put": "update", "get": "retrieve", "delete": "destroy"}
        ),
    ),
]

# 视图集: ReadOnlyModelViewSet
student_v9 = [
    path(
        "students/", StudentReadOnlyViewSet.as_view({"get": "list", "post": "create"})
    ),
    re_path(
        "^students/(?P<pk>\d+)/$",
        StudentReadOnlyViewSet.as_view(
            {"put": "update", "get": "retrieve", "delete": "destroy"}
        ),
    ),
]

# 视图集: ModelViewSet  --->俗称万能视图集
student_v10 = [
    path("students/", StudentModelViewSet.as_view({"get": "list", "post": "create"})),
    re_path(
        "^students/(?P<pk>\d+)/$",
        StudentModelViewSet.as_view(
            {"put": "update", "get": "retrieve", "delete": "destroy"}
        ),
    ),
]

urlpatterns = [
    # path("students/", StudentAPIView.as_view()),
    # re_path("^students/(?P<pk>\d+)/$", StudentInfoAPIView.as_view())
    re_path("api/v1/", include(student_v1)),
    re_path("api/v2/", include(student_v2)),
    re_path("api/v3/", include(student_v3)),
    re_path("api/v4/", include(student_v4)),
    re_path("api/v5/", include(student_v5)),
    re_path("api/v6/", include(student_v6)),
    re_path("api/v7/", include(student_v7)),
    re_path("api/v8/", include(student_v8)),
    re_path("api/v9/", include(student_v9)),
    re_path("api/v10/", include(student_v10)),
]

"""
虽然使用 ModelViewSet 可以把视图函数精简到两行，但是路由配置代码确变得复杂了，drf里面有自动生成路由的组件
"""

# 自动生成路由信息【和视图集一起使用】
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1.实例化路由类
router = SimpleRouter()

# 2. 给路由去注册视图集
router.register("api/v11/students", StudentModelViewSet, basename="api/v11/students")
# print(router.urls)

# 3.把生成的路由列表和 urlpatterns 进行拼接

urlpatterns += router.urls
