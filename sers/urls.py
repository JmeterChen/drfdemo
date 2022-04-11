# -*- coding:utf-8 -*-
"""
@Date   : 2022/3/23
@File   : urls
@Author : chenwenjian.bolin
"""


from django.urls import path
from sers.views import UsersView


urlpatterns = [
    path("user/", UsersView.as_view())
]