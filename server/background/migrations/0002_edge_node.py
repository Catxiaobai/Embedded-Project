# Generated by Django 3.1.1 on 2021-06-25 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0016_variable_length'),
        ('background', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', unique=True)),
                ('label', models.TextField(default='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.item')),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('event', models.TextField(default='')),
                ('condition', models.TextField(default='')),
                ('action', models.TextField(default='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.item')),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='src', to='background.node')),
                ('tgt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tgt', to='background.node')),
            ],
        ),
    ]