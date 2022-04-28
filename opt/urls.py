# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-17

from django.urls import path
from opt.views import ExampleView
from rest_framework.routers import DefaultRouter
from opt.views import OptModelViewSet, OptAPIView, OptGenericAPIView, OptMixinAPIView

router = DefaultRouter()
router.register("api/v2", OptModelViewSet, "v2")

urlpatterns = [
    path("api/v1/example/", ExampleView.as_view()),
    path("api/v3/", OptAPIView.as_view()),
    path("api/v4/", OptGenericAPIView.as_view()),
    path("api/v5/", OptMixinAPIView.as_view()),
]

urlpatterns += router.urls
