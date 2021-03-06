# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbUser(models.Model):
    name = models.CharField(max_length=64, verbose_name="姓名")
    employee_id = models.BigIntegerField()
    age = models.CharField(max_length=8, verbose_name="年龄")
    sex = models.BooleanField(default=1, verbose_name="性别")
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=0, verbose_name="是否已删除")

    class Meta:
        managed = False
        db_table = "tb_user"
