from rest_framework import serializers
from .models import Category, Course
from django_filters import rest_framework as filters

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['course_id','name','url','key','description','image','category','rating','reviews','students','language','author','isActive','catelog']



class CategorySerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)
    class Meta:
        model = Category
        fields = ['cat_id','name','description','courses','identifier', 'isActive']

class CategorySerializerWithoutCourses(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cat_id','name','key','description','identifier', 'isActive']


