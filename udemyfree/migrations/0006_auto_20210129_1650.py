# Generated by Django 3.1.5 on 2021-01-29 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udemyfree', '0005_auto_20210129_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]