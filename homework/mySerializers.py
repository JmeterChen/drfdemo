# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-15


from rest_framework import serializers
from homework.models import Course


class CourseModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        # fields = ["product_id", "product_name", "operator"]
