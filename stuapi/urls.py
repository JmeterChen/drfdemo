# -*- coding:utf-8 -*-
"""
@Date   : 2022/3/13
@File   : urls.py
@Author : chenwenjian.bolin
"""

from django.urls import path, re_path
from stuapi.views import StudentView, StudentInfoView

urlpatterns = [
    path("students/", StudentView.as_view()),
    re_path("^students/(?P<pk>\d+)/$", StudentInfoView.as_view()),
]
