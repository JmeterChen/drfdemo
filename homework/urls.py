# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-15

from django.urls import path, re_path, include

# 使用 APIView 视图类实现
from homework.views import CourseAPIView, CourseInfoAPIView

# 使用 GenericAPIView 视图类实现
from homework.views import CourseGenericAPIView, CourseInfoGenericAPIView

# 使用 GenericAPIView + Mixin 视图类实现
from homework.views import CourseGenericMixinAPIView, CourseGenericMixinInfoAPIView

course_v1 = [
    path("course/", CourseAPIView.as_view()),
    re_path("^course/(?P<pk>\d+)/$", CourseInfoAPIView.as_view()),
]

course_v2 = [
    path("course/", CourseGenericAPIView.as_view()),
    re_path("^course/(?P<pk>\d+)/$", CourseInfoGenericAPIView.as_view()),
]

course_v3 = [
    path("course/", CourseGenericMixinAPIView.as_view()),
    re_path("^course/(?P<pk>\d+)/$", CourseGenericMixinInfoAPIView.as_view()),
]

urlpatterns = [
    re_path("api/v1/", include(course_v1)),
    re_path("api/v2/", include(course_v2)),
    re_path("api/v3/", include(course_v3)),
]
