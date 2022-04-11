# -*- coding:utf-8 -*-
"""
@Date   : 2022/3/22
@File   : mySerializers
@Author : chenwenjian.bolin
"""

from rest_framework import serializers
from sers.models import TbUser

"""
serializer 是drf提供给开发者调用的序列化器模块
里面声明了所有的可用序列化器的基类：
Serializer          序列化器基类，drf中所有的序列化器类都必须继承于Serializer
ModelSerializer     模型序列化器基类，是序列化器基类的子类，在工作中，除了Serializer基类以外，最常用的序列化器类基类
"""


class User1Serializers(serializers.Serializer):
    """User信息序列化器
    作用:
        将模型对象数据 进行序列化后 输出返回给客户端
    """

    # 最多写四种不同的代码类型
    # 1. 转换的字段声明
    # 返回给客户端字段 = 字段类型(选项=选项值,)
    id = serializers.IntegerField()
    name = serializers.CharField()
    employee_id = serializers.IntegerField()
    age = serializers.CharField()
    sex = serializers.BooleanField()
    create_time = serializers.DateTimeField()
    modify_time = serializers.DateTimeField()
    is_delete = serializers.BooleanField()

    # 2. 如果当前的序列化器继承的是 ModelSerializer， 则需要声明调用的模型信息
    # class Meta:
    #     model = 模型名
    #     field = ["字段1", "字段2", ...]

    # 3.验证代码的对象方法
    # def validate(self, attrs):  # 函数名 validate 是固定的
    #     return attrs
    #
    # def validate_字段名(self, data):  # 方法名的格式必须是以 validate_<字段名>的形式，否则序列化器不能识别！
    #     return data

    # 4. 模型操作的方法        # 完成添加操作，添加数据以后，就自动实现了从字典变成模型对象的过程
    # def create(self, validate_data):
    #     pass
    #
    # def update(self, instance, validate_data):  # 完成更新数据操作，更新数据完成后，就自动实现了从字典变成模型对象的过程
    #     pass


# 3.3 自定义方法，然后在序列化器类字段中 通过 validators=[func_name] 的形式进行添加校验逻辑
def check_name_prefix(data):
    """
    :param data:
    :return:
    """
    if data.startswith("hello"):
        raise serializers.ValidationError(detail="姓名不可以以hello开头", code="check_name_prefix")
    return data


class User2Serializers(serializers.Serializer):
    """User信息序列化器
    作用:
        将模型对象数据 进行序列化后 输出返回给客户端
        将客户端请求数据反序列化 然后进行数据校验
    """

    # 最多写四种不同的代码类型
    # 1. 转换的字段声明
    # 返回给客户端字段 = serializers.字段类型(选项=选项值,)
    id = serializers.IntegerField(read_only=True)  # 表明该字段仅用于序列化输出，默认为False
    # validators 外部验证函数选项，值是一个列表，列表得到的成员是函数名，不能是字符串！
    name = serializers.CharField(required=True, validators=[check_name_prefix])  # 表明该字段用于反序列化输入校验为必填，默认为False
    employee_id = serializers.IntegerField(max_value=999999, min_value=420000,
                                           # 这里可以添加 error_messages 参数，当指定请求参数不符合校验时，提示相应报错。
                                           error_messages={
                                               "min_value": "The value of employee_id Must be >= 420000",
                                               "max_value": "The value of employee_id Must be <= 999999",
                                           })  #
    age = serializers.CharField(max_length=3, min_length=1)
    sex = serializers.BooleanField()
    create_time = serializers.DateTimeField(read_only=True)
    modify_time = serializers.DateTimeField(read_only=True)
    is_delete = serializers.BooleanField(default=False)

    # 2. 如果当前的序列化器继承的是 ModelSerializer， 则需要声明调用的模型信息
    # class Meta:
    #     model = 模型名
    #     field = ["字段1", "字段2", ...]

    # 3.验证代码的对象方法
    # 3.1获取客户端所有的参数，进行定制化校验逻辑
    def validate(self, attrs):
        """接受客户端的所有数据
        函数名 validate 是固定的
        :param attrs       是序列化器实例化时的data选项数据，即可以拿到客户端请求的所有参数
        """
        print(f"参数attrs: {attrs}")
        # 举例场景： 参数中多个关联的参数存在限制的时候就可以用此方法校验函数
        # 比如前端注册账号的时候，可以校验密码和确认密码是否一致等
        return attrs

    # 3.2 根据方法名中的 name 自动获取客户端请求中对应的参数 进行定制化校验逻辑
    def validate_name(self, data):  # 方法名的格式必须是以 validate_<字段名>的形式，否则序列化器不能识别！
        """验证单个字段
        validate开头的方法，会自动被is_valid调用的
        该种方法就 拓展了在内置参数的功能，比如上面age 建表的时候类型时字符串，但是我想让age的范围是在0-150，CharField又不存在该功能
        时就可以在这种方法内将类型转换再加以限制,详情见下述 validate_age 方法
        """
        print(f"data:{data}")
        if data in ["Kobe", "James", "Jordan"]:
            # 在序列化器中，验证失败可以通过抛出异常的方式来告知 is_valid
            raise serializers.ValidationError(detail="姓名不可以是Kobe、James or Jordan", code="validate_name")
        return data

    def validate_age(self, data):
        _data = int(data)
        if _data >= 150:
            raise serializers.ValidationError(detail="age 最大为150 岁", code="validate_age")
        if _data < 0:
            raise serializers.ValidationError(detail="age 最小为0 岁", code="validate_age")
        return data

    # 4. 模型操作的方法        # 完成添加操作，添加数据以后，就自动实现了从字典变成模型对象的过程
    def create(self, validate_data):
        """
        添加数据，方法名固定为 create， 固定参数 validate_data 就是验证成功以后的结果
        :param validate_data:
        :return:
        """
        user = TbUser.objects.create(**validate_data)
        return user

    #
    def update(self, instance, validate_data):  # 完成更新数据操作，更新数据完成后，就自动实现了从字典变成模型对象的过程
        """
        更新数据操作
        方法名固定为 update， 数据更新以后，就自动实现了从字段变成模型对象的过程
        :param instance:            实例化序列化器对象时，必须传入的模型对象
        :param validate_data:       就是验证成功以后的结果
        :return:
        """
        print("update_validate_data:", validate_data)
        for key, value in validate_data.items():
            setattr(instance, key, value)
        instance.save()  # 调用模型对象的 save 方法, 这里的save 其实模型对象的 save 与 serializer.save()不是同一个类的方法
        return instance
