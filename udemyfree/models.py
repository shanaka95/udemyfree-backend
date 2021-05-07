from django.db import models

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100, null=True)
    name = models.CharField( max_length=255,null=True)
    identifier = models.CharField(max_length=100, null=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)
    catelog = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='courses')
    rating  = models.FloatField(null=True)
    reviews = models.IntegerField(null=True)
    students = models.IntegerField(null=True)
    language = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True, null=True)
    isActive = models.BooleanField(default=True, null=True)


    def __str__(self):
        return self.name

class ExpiredCourse(models.Model):
    course_id = models.IntegerField(primary_key=True)
    name = models.CharField( max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)
    catelog = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='courses2')
    rating  = models.FloatField(null=True)
    reviews = models.IntegerField(null=True)
    students = models.IntegerField(null=True)
    language = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    deletedAt = models.DateTimeField("Deleted At", auto_now_add=True, null=True)
    isActive = models.BooleanField(default=False, null=True)


    def __str__(self):
        return self.name


