# Generated by Django 3.2.12 on 2023-04-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20230423_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_models',
            name='skills',
        ),
        migrations.AlterField(
            model_name='student_models',
            name='password',
            field=models.CharField(default='LwUWZiK', max_length=20),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='password',
            field=models.CharField(default='uNgLdfl', max_length=20),
        ),
    ]
