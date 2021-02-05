"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from udemyfree.views import CategoryView, CategoryPostsView, CategoryOnlyView, CourseView, AdminCourseView, \
    AdminCourseDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', CategoryView.as_view()),
    path('category/<id>', CategoryPostsView.as_view()),
    path('categories/all', CategoryOnlyView.as_view()),
    path('course/<id>', CourseView.as_view()),
    path('admin/courses/check', AdminCourseDeleteView.as_view()),
    path('admin/courses', AdminCourseView.as_view())
]
