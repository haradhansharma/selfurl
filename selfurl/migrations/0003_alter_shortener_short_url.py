# Generated by Django 4.0.3 on 2022-03-21 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfurl', '0002_alter_shortener_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortener',
            name='short_url',
            field=models.SlugField(max_length=15, unique=True),
        ),
    ]
