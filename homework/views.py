from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from homework.models import Course
from homework.mySerializers import CourseModelSerializers
from rest_framework import status
from rest_framework.generics import GenericAPIView


# APIView 实现 5个 api 接口
class CourseAPIView(APIView):
	def get(self, request):
		# 1.获取数据库中内容
		db_data = Course.objects.all()
		
		# 2. 实例化序列化器,获取序列化对象
		serializer = CourseModelSerializers(instance=db_data, many=True)
		
		# 3. 序列化从数据库中得到的内容并返回给客户端
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		# 1.获取请求内容
		req_data = request.data
		
		# 2.实例化序列化器,获取序列化对象
		serializer = CourseModelSerializers(data=req_data)
		
		# 3.反序列化[验证数据、保存数据到数据库]
		print(serializer.is_valid())
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		
		# 4.返回新增的模型数据到客户端
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseInfoAPIView(APIView):
	def get(self, request, pk):
		"""获取一条学生信息"""
		# 1. 使用pk作为条件获取模型对象
		try:
			student = Course.objects.get(id=pk)
			print(type(student))
		except Course.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2. 序列化
		serializer = CourseModelSerializers(instance=student)
		
		# 3.返回结果
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象
		try:
			student = Course.objects.get(id=pk)
		except Course.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2.获取客户端提交的数据
		
		req_data = request.data
		# 3.反序列化【验证数据和数据保存】
		serializer = CourseModelSerializers(instance=student, data=req_data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		# 4.返回结果
		return Response(data=serializer.data, status=status.HTTP_200_OK)
	
	def delete(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象 直接删除，并且接口是幂等的！
		try:
			student = Course.objects.get(id=pk).delete()
		except Course.DoesNotExist:
			pass
		
		return Response(status=status.HTTP_204_NO_CONTENT)


# GenericAPIView 实现 5个 api 接口
class CourseGenericAPIView(GenericAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseModelSerializers
	
	def get(self, request):
		# 1. 从数据库中读取学生列表信息
		instance = self.get_queryset()  # GenericAPIView提供的 get_queryset
		# 2. 序列化
		serializer = self.get_serializer(instance=instance, many=True)
		
		# 3.转换数据并返回给客户端
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		# 1.获取请求内容
		req_data = request.data
		
		# 2.实例化序列化器,获取序列化对象
		serializer = self.get_serializer(data=req_data)
		
		# 3.反序列化[验证数据、保存数据到数据库]
		# print(serializer.is_valid())
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		
		# 4.返回新增的模型数据到客户端
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseInfoGenericAPIView(GenericAPIView):
	queryset = Course.objects.all()
	serializer_class = CourseModelSerializers
	
	def get(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		# 2.序列化
		serializer = self.get_serializer(instance=instance)
		# 3. 返回结果
		return Response(serializer.data)
	
	def put(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		# 2. 序列化和数据校验
		serializer = self.get_serializer(instance=instance, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		# 3.返回客户端结果
		return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
	
	def delete(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		instance.delete()
		return Response(status.HTTP_200_OK)


# GenericAPIView + Mixins
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin


class CourseGenericMixinAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
	queryset = Course.objects.all()
	serializer_class = CourseModelSerializers
	
	def get(self, request):
		return self.list(request)
	
	def post(self, request):
		return self.create(request)


class CourseGenericMixinInfoAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
	queryset = Course.objects.all()
	serializer_class = CourseModelSerializers
	
	def get(self, request, pk):
		return self.retrieve(request, pk)
	
	def put(self, request, pk):
		return self.update(request, pk)
	
	def delete(self, request, pk):
		return self.destroy(request, pk)
