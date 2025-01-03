# Generated by Django 5.0.7 on 2025-01-02 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='生日'),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='员工编号'),
        ),
        migrations.AddField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(blank=True, null=True, verbose_name='入职日期'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='电话号码'),
        ),
    ]
