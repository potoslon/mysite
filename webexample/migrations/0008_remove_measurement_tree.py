# Generated by Django 3.1.1 on 2020-12-12 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webexample', '0007_remove_measurement_shops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='tree',
        ),
    ]
