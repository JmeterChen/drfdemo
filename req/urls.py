# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-06


from django.urls import path
from .views import StudentView, StudentAPIView

urlpatterns = [
    path("student/v1/", StudentView.as_view()),
    path("student/v2/", StudentAPIView.as_view())
]