# Generated by Django 4.0.3 on 2022-03-23 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exsite',
            name='site_meta_tag',
        ),
    ]
