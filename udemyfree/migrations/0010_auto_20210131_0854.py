# Generated by Django 3.1.5 on 2021-01-31 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udemyfree', '0009_course_catelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='key',
            field=models.CharField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='url',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
