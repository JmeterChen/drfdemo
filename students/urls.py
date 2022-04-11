# -*- coding:utf-8 -*-
"""
@Date   : 2022/3/14
@File   : urls.py
@Author : chenwenjian.bolin
"""

from rest_framework.routers import DefaultRouter
from students.views import StudentModelViewSet

router = DefaultRouter()
router.register("stu", StudentModelViewSet, basename="stu_restful_api")

urlpatterns = [

              ] + router.urls
