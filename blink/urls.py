"""
URL configuration for blink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# swagger 관련 ( 참고 : https://velog.io/@emrrbs9090/DjangoSwagger-with-DRFyasg )
from drf-yasg.views import get_schema_view
from drf-yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your Server Name or Swagger Docs name",
        default_version="Your API version(Custom)",
        description="Your Swagger Docs descriptions",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="test", email="test@test.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # swagger 관련 ( 참고 : https://velog.io/@emrrbs9090/DjangoSwagger-with-DRFyasg )
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
