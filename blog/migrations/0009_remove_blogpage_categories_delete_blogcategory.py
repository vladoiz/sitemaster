# Generated by Django 4.0.7 on 2022-09-18 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogcategory_blogpage_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='categories',
        ),
        migrations.DeleteModel(
            name='BlogCategory',
        ),
    ]
