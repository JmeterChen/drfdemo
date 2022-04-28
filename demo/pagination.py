# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2022-04-19


from rest_framework.pagination import PageNumberPagination


class GeneralPaginator(PageNumberPagination):
    # 默认每页显示的数据条数
    page_size = 2

    # 获取URL参数中的设置页数
    page_query_param = "page_number"
    # 获取URL参数中的设置的每页显示数据条数
    page_size_query_param = "page_size"
    # 最大支持的每页显示的条数
    max_page_size = 999
