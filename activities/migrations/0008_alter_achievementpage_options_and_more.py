# Generated by Django 4.0.10 on 2024-06-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_alter_achievementpage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achievementpage',
            options={},
        ),
        migrations.AlterField(
            model_name='activityindexpage',
            name='intro',
            field=models.TextField(blank=True),
        ),
    ]
