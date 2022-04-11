# -*- coding:utf-8 -*-
"""
@Date   : 2022/3/13
@File   : serializers
@Author : chenwenjian.bolin
"""

from rest_framework import serializers
from stuapi.models import Student


class StudentModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        # fields = ["product_id", "product_name", "operator"]
        extra_kwargs = {
            "age": {
                "max_value": 25,
                "error_messages": {
                    "max_value": "年龄不能超过25岁！"
                }
            }
        }
