# Generated by Django 3.1.1 on 2021-05-09 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '0004_paths'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, default='')),
                ('type2', models.TextField(blank=True, default='')),
                ('name', models.TextField(blank=True, default='')),
                ('paths', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.paths')),
            ],
        ),
    ]
