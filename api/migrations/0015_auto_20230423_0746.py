# Generated by Django 3.2.12 on 2023-04-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20230423_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_models',
            name='password',
            field=models.CharField(default='bN7qjYg', max_length=20),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='password',
            field=models.CharField(default='M2ABc16', max_length=20),
        ),
    ]
