# Generated by Django 3.1.5 on 2021-01-31 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udemyfree', '0010_auto_20210131_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='key',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='url',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
