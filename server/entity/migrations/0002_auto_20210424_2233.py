# Generated by Django 3.1.1 on 2021-04-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='item_content',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='item_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='item_describe',
            new_name='path',
        ),
        migrations.AddField(
            model_name='item',
            name='describe',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='item',
            name='software',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='item',
            name='team',
            field=models.TextField(default=''),
        ),
    ]
