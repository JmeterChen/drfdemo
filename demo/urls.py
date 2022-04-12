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
from .views import StudentViewSet, StudentInfoViewSet

student_v1 = [
    path("students/", StudentAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoAPIView.as_view()),
]

student_v2 = [
    path("students/", StudentGenericAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoGenericAPIView.as_view())
]

student_v3 = [
    path("students/", StudentMixinAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoMixinAPIView.as_view())
]

# 视图子类1
student_v4 = [
    path("students/", StudentView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoView.as_view())
]

# 视图子类2
student_v5 = [
    path("students/", StudentSimpleView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentSimpleInfoView.as_view())
]


# 视图集
student_v6 = [
    path("students/", StudentViewSet.as_view({
	    "get": "get_list",
	    "post": "post"
    })),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoViewSet.as_view({
	    "put": "put",
	    "get": "get_student_info",
	    "delete": "delete"
    }))
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
]
