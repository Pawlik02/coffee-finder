# Generated by Django 3.0.6 on 2020-06-02 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_finder', '0012_auto_20200602_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='my_places',
            new_name='my_place',
        ),
    ]