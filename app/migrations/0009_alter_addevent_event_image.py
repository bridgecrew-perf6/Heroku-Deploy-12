# Generated by Django 4.0.4 on 2022-06-13 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_eventcomment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addevent',
            name='event_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
