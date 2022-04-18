# Generated by Django 3.2.4 on 2022-04-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='课程名称 ')),
                ('description', models.TextField(max_length=1000, verbose_name='简介')),
                ('out_time', models.TimeField(verbose_name='下课时间')),
                ('on_time', models.TimeField(verbose_name='上课时间')),
                ('duration', models.DurationField(verbose_name='课时')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格')),
            ],
            options={
                'verbose_name': '课程信息',
                'verbose_name_plural': '课程信息',
                'db_table': 'hk_course',
            },
        ),
    ]