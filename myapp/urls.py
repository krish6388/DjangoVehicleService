from django.contrib import admin
from django.urls import path
from myapp.views import create_issue, home, resolve_issue,close_issue

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_issue/', create_issue, name='create_issue'),
    path('', home, name='home'),
    path('resolve_issue/', resolve_issue, name='resolve_issue'),
    path('close_issue/', close_issue, name='close_issue'),
]
