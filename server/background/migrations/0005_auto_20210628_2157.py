# Generated by Django 3.1.1 on 2021-06-28 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0004_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='url',
            new_name='src',
        ),
    ]
