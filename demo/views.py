from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from stuapi.models import Student
from students.mySerializers import StudentModelSerializers
from rest_framework import status

from rest_framework.generics import GenericAPIView

"""
GET:        获取所有学生信息
POST:       新增一个学生信息

PUT:        修改一个学生信息
DELETE:     删除一个学生信息
GET:        获取指定学生信息
"""

"""APIView基本视图类"""


class StudentAPIView(APIView):
	
	def get(self, request):
		# 1.获取数据库中内容
		db_data = Student.objects.all()
		
		# 2. 实例化序列化器,获取序列化对象
		serializer = StudentModelSerializers(instance=db_data, many=True)
		
		# 3. 序列化从数据库中得到的内容并返回给客户端
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		# 1.获取请求内容
		req_data = request.data
		
		# 2.实例化序列化器,获取序列化对象
		serializer = StudentModelSerializers(data=req_data)
		
		# 3.反序列化[验证数据、保存数据到数据库]
		print(serializer.is_valid())
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		
		# 4.返回新增的模型数据到客户端
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoAPIView(APIView):
	def get(self, request, pk):
		"""获取一条学生信息"""
		# 1. 使用pk作为条件获取模型对象
		try:
			# student = Student.objects.filter(id=pk)   # 这里注意 filter 返回的是 <class 'django.db.models.query.QuerySet'> 对象
			# print(type(student))
			student = Student.objects.get(id=pk)  # 这里注意用 get 方法返回的是 <class 'stuapi.models.Student'> 对象
			print(type(student))
		except Student.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2. 序列化
		serializer = StudentModelSerializers(instance=student)
		
		# 3.返回结果
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象
		try:
			# student = Student.objects.filter(id=pk)   # 这里注意 filter 返回的是 <class 'django.db.models.query.QuerySet'> 对象
			# print(type(student))
			student = Student.objects.get(id=pk)  # 这里注意用 get 方法返回的是 <class 'stuapi.models.Student'> 对象
		# print(type(student))
		except Student.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2.获取客户端提交的数据
		
		req_data = request.data
		
		# 3.反序列化【验证数据和数据保存】
		serializer = StudentModelSerializers(instance=student, data=req_data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		# 4.返回结果
		return Response(data=serializer.data, status=status.HTTP_200_OK)
	
	def delete(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象 直接删除，并且接口是幂等的！
		try:
			student = Student.objects.get(id=pk).delete()
			print(type(student))
		except Student.DoesNotExist:
			pass
		
		return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericAPIView 通用视图类"""


class StudentGenericAPIView(GenericAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
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


class StudentInfoGenericAPIView(GenericAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
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


"""
使用drf内置的模型扩展类[混入类]结合 GenericAPIView 实现通用视图方法的简写操作
from rest_framework.mixins import ListModelMixin            获取多条数据，返回响应结果   list
from rest_framework.mixins import CreateModelMixin          添加一条数据，返回响应结果   create
from rest_framework.mixins import RetrieveModelMixin        获取一条数据，返回响应结果   retrieve
from rest_framework.mixins import UpdateModelMixin          更新一条数据，返回响应结果   update[更新全部字段] partial_update[更新部分字段]
from rest_framework.mixins import DestroyModelMixin         删除一条数据，返回响应结果   destroy
"""

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin


class StudentMixinAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
	def get(self, request):
		return self.list(request)
	
	def post(self, request):
		return self.create(request)


class StudentInfoMixinAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
	def get(self, request, pk):
		return self.retrieve(request, pk=pk)
	
	def put(self, request, pk):
		return self.update(request, pk)
	
	def delete(self, request, pk):
		return self.destroy(request, pk=pk)


"""
上面的接口代码还可以继续更加的精简， drf在使用 GenericAPIView 和 Mixins 进行组合以后，还提供了视图子类。
视图子类是通用的视图类和模型扩展类的子类， 提供了各种的视图方法调用 mixins 操作

    ListAPIView = GenericAPIView + ListModelMixin           获取多条数据
    CreateAPIView = GenericAPIView + CreateModelMixin       添加一条数据
    RetrieveAPIView = GenericAPIView + RetrieveModelMixin   获取一条数据
    UpdateAPIView = GenericAPIView + UpdateModelMixin       修改一条数据
    DestroyAPIView = GenericAPIView + DestroyModelMixin     删除一条数据
"""

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


class StudentView(ListAPIView, CreateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


class StudentInfoView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


"""
组合视图子类
    ListCreateAPIView = ListAPIView + CreateAPIView
    RetrieveUpdateAPIView = RetrieveAPIView + UpdateAPIView
    RetrieveDestroyAPIView = RetrieveAPIView + DestroyAPIView
    =====>
    RetrieveUpdateDestroyAPIView = RetrieveAPIView + UpdateAPIView + DestroyAPIView
"""

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class StudentSimpleView(ListCreateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


class StudentSimpleInfoView(RetrieveUpdateDestroyAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


"""
上面的接口在实现过程中，也存在了代码重复的情况，如果我们合并成一个接口类，则需要考虑两个问题：
1. 路由的合并问题；因为路由指定视图类
2. get 方法重复问题；


drf 提供了视图集可以解决上面的问题
ViewSet  --> 基本视图集  解决了 APIView 中的代码重复问题
"""

from rest_framework.viewsets import ViewSet


class StudentViewSet(ViewSet):
	
	def get_list(self, request):
		# 1.获取数据库中内容
		db_data = Student.objects.all()
		
		# 2. 实例化序列化器,获取序列化对象
		serializer = StudentModelSerializers(instance=db_data, many=True)
		
		# 3. 序列化从数据库中得到的内容并返回给客户端
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		# 1.获取请求内容
		req_data = request.data
		
		# 2.实例化序列化器,获取序列化对象
		serializer = StudentModelSerializers(data=req_data)
		
		# 3.反序列化[验证数据、保存数据到数据库]
		print(serializer.is_valid())
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		
		# 4.返回新增的模型数据到客户端
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	def get_student_info(self, request, pk):
		"""获取一条学生信息"""
		# 1. 使用pk作为条件获取模型对象
		try:
			# student = Student.objects.filter(id=pk)   # 这里注意 filter 返回的是 <class 'django.db.models.query.QuerySet'> 对象
			# print(type(student))
			student = Student.objects.get(id=pk)  # 这里注意用 get 方法返回的是 <class 'stuapi.models.Student'> 对象
			print(type(student))
		except Student.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2. 序列化
		serializer = StudentModelSerializers(instance=student)
		
		# 3.返回结果
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象
		try:
			# student = Student.objects.filter(id=pk)   # 这里注意 filter 返回的是 <class 'django.db.models.query.QuerySet'> 对象
			# print(type(student))
			student = Student.objects.get(id=pk)  # 这里注意用 get 方法返回的是 <class 'stuapi.models.Student'> 对象
		# print(type(student))
		except Student.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		# 2.获取客户端提交的数据
		
		req_data = request.data
		
		# 3.反序列化【验证数据和数据保存】
		serializer = StudentModelSerializers(instance=student, data=req_data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		
		# 4.返回结果
		return Response(data=serializer.data, status=status.HTTP_200_OK)
	
	def delete(self, request, pk):
		# 1.使用 pk 作为条件获取模型对象 直接删除，并且接口是幂等的！
		try:
			student = Student.objects.get(id=pk).delete()
			print(type(student))
		except Student.DoesNotExist:
			pass
		
		return Response(status=status.HTTP_204_NO_CONTENT)


"""
GenericViewSet  --> 通用视图集  解决了 APIView 中的代码重复问题，同时让代码更加通用
"""

from rest_framework.viewsets import GenericViewSet


class StudentGenericViewSet(GenericViewSet):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
	def list(self, request):
		# 1. 从数据库中读取学生列表信息
		instance = self.get_queryset()  # GenericAPIView提供的 get_queryset
		# 2. 序列化
		serializer = self.get_serializer(instance=instance, many=True)
		
		# 3.转换数据并返回给客户端
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def create(self, request):
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
	
	def retrieve(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		# 2.序列化
		serializer = self.get_serializer(instance=instance)
		# 3. 返回结果
		return Response(serializer.data)
	
	def update(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		# 2. 序列化和数据校验
		serializer = self.get_serializer(instance=instance, data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
		# 3.返回客户端结果
		return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
	
	def destroy(self, request, pk):
		# 1. 使用pk作为条件获取模型对象
		instance = self.get_object()
		instance.delete()
		return Response(status.HTTP_200_OK)


"""
写到这里 我们发现自定义的方法名好像在 mixins 组件类中出现过， 那么只要将对应的类继承，就不需要声明对应的方法了
故：
GenericViewSet 通用视图集 + 混入类即（mixins 组件类)
"""

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin


class StudentMixinViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                          DestroyModelMixin):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


"""
上面的接口类看起来已经通过几行代码实现了最初的100+代码的工作量，但是继承了太多父类，还可以继续优化
我们可以继续让一些已经合并的视图集父类让接口类继承即可
ReadOnlyModelViewSet = mixins.RetrieveModelMixin + mixins.ListModelMixin + GenericViewSet
	获取多条数据
	获取一条数据
"""

from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin


class StudentReadOnlyViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers


"""
既然 ReadOnlyModelViewSet 类已经合并了三个类了，那有没有合并全部6个类的类呢？
查看源码，其实是有的，那就是 ModelViewSet

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
	'''
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    '''
    pass

"""

from rest_framework.viewsets import ModelViewSet


class StudentModelViewSet(ModelViewSet):  # 万能视图集
	queryset = Student.objects.all()
	serializer_class = StudentModelSerializers
	
	"""
	使用上述 ModelViewSet 写法可以很快速的写出 某种对象的增删改查的接口，但是如果需要针对学生再加上比如登录的接口，那么新写一个
	视图类好像有点多余，并且还要额外去定义路由，那么久失去了 drf 的简洁的特性了 drf 其实提供了这个能力
	在视图集中附加 action 的声明
	"""
	
	from rest_framework.decorators import action
	
	"""
	action 装饰器接受参数：
		- methods       required    声明该 action 对应请求的方法， 列表传递
		- detail        required    声明该 action 的路径是否与单一资源对应
			True    表示路径是 xxx/<pk>/action方法名/url_path
			False   表示路径是 xxx/action方法名/url_path
		- url_path:     optional    声明该 action 的路由尾缀, 定义的路径会把 action方法名在path的内容覆盖
			例如：
			 声明了 url_path，则path 为 students/<pk>/user/login/
			 未声明 url_path，则path 为 students/<pk>/login/
	"""
	
	@action(methods=["get"], detail=True, url_path="user/login")    #
	def login(self, request, pk):
		print("登录成功")
		return Response({"msg": "ok"})
