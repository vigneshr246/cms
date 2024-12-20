# Generated by Django 5.1.4 on 2024-12-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_userpermission_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.CharField(default='admin', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default='user', max_length=50),
        ),
    ]
