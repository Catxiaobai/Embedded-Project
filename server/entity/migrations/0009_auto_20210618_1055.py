# Generated by Django 3.1.1 on 2021-06-18 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0008_auto_20210618_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protocol',
            name='check_method',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='frame_header',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='frame_tail',
        ),
    ]
