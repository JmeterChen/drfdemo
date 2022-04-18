from django.db import models


# Create your models here.
class Course(models.Model):
	"""学生信息"""
	name = models.CharField(max_length=255, verbose_name="课程名称 ")
	description = models.TextField(max_length=1000, verbose_name="简介")
	out_time = models.TimeField(verbose_name="下课时间")
	on_time = models.TimeField(verbose_name="上课时间")
	duration = models.DurationField(verbose_name="课时")
	price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="价格")
	
	class Meta:
		db_table = "hk_course"
		verbose_name = "课程信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.name
