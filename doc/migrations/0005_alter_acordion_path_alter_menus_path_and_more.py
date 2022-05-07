# Generated by Django 4.0.3 on 2022-04-02 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0004_alter_acordion_path_alter_menus_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acordion',
            name='path',
            field=models.CharField(choices=[('selfurl:index', 'Index'), ('selfurl:report_malicious', 'Report_malicious'), ('selfurl:click_counter', 'Click_counter'), ('selfurl:redirect_url', 'Redirect_url'), ('contact:contact', 'Contact'), ('doc:webmanifest', 'Webmanifest'), ('doc:terms_and_conditions', 'Terms_and_conditions'), ('doc:privacy_policy', 'Privacy_policy')], max_length=50),
        ),
        migrations.AlterField(
            model_name='menus',
            name='path',
            field=models.CharField(choices=[('selfurl:index', 'Index'), ('selfurl:report_malicious', 'Report_malicious'), ('selfurl:click_counter', 'Click_counter'), ('selfurl:redirect_url', 'Redirect_url'), ('contact:contact', 'Contact'), ('doc:webmanifest', 'Webmanifest'), ('doc:terms_and_conditions', 'Terms_and_conditions'), ('doc:privacy_policy', 'Privacy_policy')], max_length=50),
        ),
        migrations.AlterField(
            model_name='metatext',
            name='path',
            field=models.CharField(choices=[('selfurl:index', 'Index'), ('selfurl:report_malicious', 'Report_malicious'), ('selfurl:click_counter', 'Click_counter'), ('selfurl:redirect_url', 'Redirect_url'), ('contact:contact', 'Contact'), ('doc:webmanifest', 'Webmanifest'), ('doc:terms_and_conditions', 'Terms_and_conditions'), ('doc:privacy_policy', 'Privacy_policy')], max_length=50),
        ),
    ]
