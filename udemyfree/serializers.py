from rest_framework import serializers
from .models import Category, Course
from django_filters import rest_framework as filters

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['course_id','name','url','key','description','image','category','rating','reviews','students','language','author','isActive','catelog']



class CategorySerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField('get_courses')

    def get_courses(self,category):
        print(category)
        qs = Course.objects.filter(isActive = True, category__name=category)
        serializer = CourseSerializer(instance=qs, many=True)
        return serializer.data
    class Meta:
        model = Category
        fields = ['cat_id','name','description','courses','identifier', 'isActive']

class CategorySerializerWithoutCourses(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cat_id','name','key','description','identifier', 'isActive']


class SiteMapCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['identifier']

class SiteMapCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['key']