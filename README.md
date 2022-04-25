# drfdemo


#### drf 自动生成 swagger 接口文档
### 1.安装依赖库

```
pip install drf-yasg
```

### 2.配置视图类

```
#  drfdemo/urls.py
# swagger 接口文档导入包
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
	openapi.Info(
		title="drf_swarg 接口文档",
		default_version="v1.0.0",
		description="接口文档",
		terms_of_service="",
		contact=openapi.Contact(email="359402852@qq.com"),
		license=openapi.License(name="MIT")
	),
	public=True,  # 允许所有人都可以访问
	# permission_classes=(IsAuthenticated,)       # 权限类
)
```
### 3. 配置视图的总路由

```
urlpatterns = [
	path('admin/', admin.site.urls),
    ...
	path("doc/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger")
]
```
