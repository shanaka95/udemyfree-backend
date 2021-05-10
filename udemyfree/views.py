from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, generics
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator

from udemyfree.models import Category, Course, ExpiredCourse
from udemyfree.serializers import CategorySerializer, CourseSerializer, CategorySerializerWithoutCourses, \
    SiteMapCoursesSerializer, SiteMapCategorySerializer
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

        if id != 'all-courses':
            courses = self.filter_queryset(self.get_queryset()).filter(category__identifier=id)
            category = Category.objects.filter(identifier=id)
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
            newCourse = ExpiredCourse()
            newCourse.course_id = course.course_id
            newCourse.name = course.name
            newCourse.image = course.image
            newCourse.category = course.category
            newCourse.author = course.author
            newCourse.catelog = course.catelog
            newCourse.description = course.description
            newCourse.key = course.key
            newCourse.isActive = 0
            newCourse.url = course.url
            newCourse.rating = course.rating
            newCourse.reviews = 0
            newCourse.language = course.language
            newCourse.students = course.students
            course.delete()
            newCourse.save()
            count = Course.objects.filter(isActive=True).count()
            return Response({"status": True, "count":count })
        else:
            return Response({"status": False})

class CrawlCategoryView(views.APIView):
    def get(self, request, id):
        if id == "all-courses":
            html = """<html>
                    <head>
                    <title>Free Udemy Courses | Daily Updated!</title>
                    <meta property="og:title" name="title" content="Free Udemy Courses | Daily Updated!">
                    <meta property="og:description" name="description" content="Find out latest Free Udemy Courses .The courses list contains 100+ courses and, is updated daily.">
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
                """
        else:
            category = Category.objects.filter(identifier=id)[0]

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


class SitemapView(views.APIView):
    content_type = 'application/xml'

    def get(self, request):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9             http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

<url>
  <loc>https://udemyfree.courses/</loc>
  <lastmod>2021-04-08T04:37:31+00:00</lastmod>
  <priority>1.00</priority>
</url>
<url>
  <loc>https://udemyfree.courses/courses/category/all-courses</loc>
  <lastmod>2021-04-08T04:37:31+00:00</lastmod>
  <priority>1.00</priority>
</url>
"""
        xml2 = """<url>
<loc>https://udemyfree.courses/add</loc>
  <lastmod>2021-04-08T04:37:31+00:00</lastmod>
  <priority>1.00</priority>
</url>
<url>
  <loc>https://udemyfree.courses/privacy-policy</loc>
  <lastmod>2021-02-20T18:28:29+00:00</lastmod>
  <priority>1.00</priority>
</url>
</urlset>
        """
        AllCategories = Category.objects.filter(isActive=True)
        serializer = SiteMapCategorySerializer(AllCategories, many=True)

        for i in serializer.data:
            date_string = datetime.today().strftime('%Y-%m-%d')
            xml += """<url>
  <loc>https://udemyfree.courses/courses/category/%s</loc>
  <lastmod>%sT06:00:00+00:00</lastmod>
  <priority>1.00</priority>
</url>""" % (i['identifier'], date_string)

        courses =  Course.objects.filter(isActive=1)
        serializer = SiteMapCoursesSerializer(courses, many=True)
        for i in serializer.data:
            date_string = datetime.today().strftime('%Y-%m-%d')
            xml += """<url>
  <loc>https://udemyfree.courses/enroll/course/%s</loc>
  <lastmod>%sT06:00:00+00:00</lastmod>
  <priority>0.80</priority>
</url>""" % (i['key'], date_string)

        xml += xml2
        return HttpResponse(xml, content_type='application/xml')