from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, generics
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator
from udemyfree.models import Category, Course
from udemyfree.serializers import CategorySerializer, CourseSerializer, CategorySerializerWithoutCourses
from rest_framework import filters

class CategoryView(views.APIView):

    def get(self, request):
        AllCategories = Category.objects.filter(isActive=True)
        serializer = CategorySerializer(AllCategories, many=True)
        for i in serializer.data:
            i['courses']= i['courses'][::-1][:8]
        return Response(serializer.data)

class CategoryOnlyView(views.APIView):

    def get(self, request):
        AllCategories = Category.objects.filter(isActive=True)
        serializer = CategorySerializerWithoutCourses(AllCategories, many=True)
        return Response(serializer.data)

class CategoryPostsView(GenericAPIView):
    queryset = Course.objects.filter(isActive=True).order_by('-createdAt')
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description','author', 'category__name']

    def get(self, request, id):
        try:
            id = int(id)
        except:
            return Response({'status': 'Invalid Request', 'error': 'Category Id is not Valid'})

        if int(id) > 0:
            courses = self.filter_queryset(self.get_queryset()).filter(category=id)
            category = Category.objects.filter(cat_id=id)
            paginator = Paginator(courses, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            serializer = CourseSerializer(page_obj, many=True)
            cat_serializer = CategorySerializerWithoutCourses(category, many=True)
            result ={'data': serializer.data, 'total': len(courses), 'category':cat_serializer.data }
        else:
            courses = self.filter_queryset(self.get_queryset())
            paginator = Paginator(courses, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            serializer = CourseSerializer(page_obj, many=True)
            result ={'data': serializer.data, 'total': len(courses), 'category':[{'name': 'All Courses'}]}
        return Response(result)



class CourseView(views.APIView):
    def get(self, request, id):
        courses =  Course.objects.filter(key=id)
        serializer = CourseSerializer(courses, many=True)
        category = Category.objects.filter(cat_id=serializer.data[0]['category'])
        cat_serializer = CategorySerializer(category, many=True)
        cat_serializer.data[0]['courses'] = cat_serializer.data[0]['courses'][::-1][:8]
        serializer.data[0]['catelog'] = serializer.data[0]['catelog'].split('^')

        return Response({'course': serializer.data, 'category': cat_serializer.data})

class AdminCourseView(views.APIView):
    def post(self, request):
        if (request.data['key'] == "%$@#GHJ854SDF53-SSdddddasda2354234VBXCSDFaseqovmgtcanrt"):
            courses = Course.objects.filter(isActive=True).order_by('createdAt')
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            return Response({})

class AdminCourseDeleteView(views.APIView):
    def post(self, request):
        if (request.data['key'] == "%$@#GHJ854SDF53-SSdddddasda2354234VBXCSDFaseqovmgtcanrt"):
            course = Course.objects.get(course_id=int(request.data['id']))
            course.isActive = False
            course.save()
            count = Course.objects.filter(isActive=True).count()
            return Response({"status": True, "count":count })
        else:
            return Response({"status": False})

class CrawlCategoryView(views.APIView):
    def get(self, request, id):
        category = Category.objects.filter(cat_id=id)[0]

        html = """<html>
                <head>
                <title>Free %s | Daily Updated!</title>
                <meta property="og:title" name="title" content="Free %s | Daily Updated!">
                <meta property="og:description" name="description" content="Find out latest Free %s .The courses list contains 100+ courses and, is updated daily.">
                <meta name="keywords" content="free online courses, udemy coupons, online courses, free courses, udemy, udemy free courses, udemy, free udemy courses,udemy courses,udemy python,udemy reviews,free courses online,online courses">
                <meta property="og:image" content="https://udemyfree.courses/images/udemyfreecourses.png" />
                <meta property="og:type" content="article" />
                <meta name="robots" content="index, follow">
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <meta name="language" content="English">
                <meta name="revisit-after" content="1 days">
                <meta name="author" content="Finlay West">
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
            </html>
            """ %(category.name,category.name,category.name)
        return HttpResponse(html)

class CrawlCourseView(views.APIView):
    def get(self, request, id):
        course = Course.objects.filter(key=id)[0]
        category = Category.objects.filter(cat_id=course.category.cat_id)[0]

        html = """<html>
                <head>
                    <title>Enroll in Udemy Course %s for Free</title>
                    <meta charset="utf-8">
                    <meta property="og:title" name="title" content="Enroll in Udemy Course %s for Free">
                    <meta property="og:description" name="description" content="Limited Time Offer | Find out more Free %s. The courses list contains 100+ courses and, is updated daily.">
                    <meta name="keywords" content="free online courses, udemy coupons, online courses, free courses, udemy, udemy free courses, udemy, free udemy courses,udemy courses,udemy python,udemy reviews,free courses online,online courses">
                    <meta property="og:type" content="article" />
                    <meta property="og:image" content="%s" />
                    <meta name="robots" content="index, follow">
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <meta name="language" content="English">
                    <meta name="revisit-after" content="1 days">
                    <meta name="author" content="Finlay West">
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
            </html>
            """ %(course.name,course.name,category.name,course.image )
        return HttpResponse(html)