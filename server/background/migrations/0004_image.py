# Generated by Django 3.1.1 on 2021-06-28 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0016_variable_length'),
        ('background', '0003_auto_20210627_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('url', models.TextField(default='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.item')),
            ],
        ),
    ]
