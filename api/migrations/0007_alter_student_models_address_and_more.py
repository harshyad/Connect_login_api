# Generated by Django 4.1.8 on 2023-04-14 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_student_models_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_models',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='branch',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='country',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='course_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='email',
            field=models.CharField(default='None', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='password',
            field=models.CharField(default='DipLO2b', max_length=20),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='roll_no',
            field=models.CharField(default='None', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_models',
            name='user_type',
            field=models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('admin', 'admin')], default='student', max_length=10),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='address',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='branch',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='country',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='course_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='email',
            field=models.CharField(default='None', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='password',
            field=models.CharField(default='ZShxJ5Q', max_length=20),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='teacher_models',
            name='user_type',
            field=models.CharField(choices=[('student', 'student'), ('teacher', 'teacher'), ('admin', 'admin')], default='teacher', max_length=10),
        ),
    ]