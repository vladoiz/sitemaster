# Generated by Django 4.0.10 on 2024-06-06 07:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('activities', '0003_alter_activitystructurepage_intro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityblogpage',
            name='blog',
        ),
        migrations.AddField(
            model_name='activityblogpage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='activityblogpage',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Post date'),
        ),
        migrations.AddField(
            model_name='activityblogpage',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AlterField(
            model_name='activityblogpage',
            name='intro',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='activityindexpage',
            name='intro',
            field=models.TextField(blank=True),
        ),
    ]
