# Generated by Django 4.0.4 on 2022-06-14 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_eventcomment_new_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcomment',
            name='new_comment',
            field=models.CharField(max_length=100),
        ),
    ]
