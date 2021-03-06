# Generated by Django 3.2.5 on 2021-11-23 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='proof',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
