# Generated by Django 4.1 on 2023-11-20 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inpatientsystemApp', '0002_operatingroom_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operatingroom',
            name='level',
        ),
    ]
