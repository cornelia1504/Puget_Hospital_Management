# Generated by Django 4.1 on 2023-11-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inpatientsystemApp', '0008_doctor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
