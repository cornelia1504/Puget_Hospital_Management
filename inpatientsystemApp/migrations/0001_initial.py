# Generated by Django 4.1 on 2023-11-14 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id_bed', models.AutoField(primary_key=True, serialize=False)),
                ('bed_department', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='doctor_profile_pic/')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id_department', models.AutoField(primary_key=True, serialize=False)),
                ('name_department', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id_doctor', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('description_doctor', models.TextField()),
                ('id_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.department')),
            ],
        ),
        migrations.CreateModel(
            name='OperatingRoom',
            fields=[
                ('id_operating_room', models.AutoField(primary_key=True, serialize=False)),
                ('class_operating_room', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id_operation', models.AutoField(primary_key=True, serialize=False)),
                ('name_operation', models.CharField(max_length=50)),
                ('date_of_operation', models.DateField()),
                ('id_operating_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.operatingroom')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id_patient', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('patient_department', models.CharField(max_length=50)),
                ('gender_patient', models.CharField(max_length=10)),
                ('id_bed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inpatientsystemApp.bed')),
                ('id_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inpatientsystemApp.department')),
                ('id_doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inpatientsystemApp.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='OperationPerforming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_operation', models.CharField(max_length=50)),
                ('date_of_operation', models.DateField()),
                ('id_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.doctor')),
                ('id_operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.operation')),
                ('id_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.patient')),
            ],
        ),
        migrations.AddField(
            model_name='operation',
            name='id_patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.patient'),
        ),
        migrations.CreateModel(
            name='OperatingRoomSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_operating_room', models.CharField(max_length=50)),
                ('scheduled_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('id_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.doctor')),
                ('id_operating_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inpatientsystemApp.operatingroom')),
            ],
        ),
        migrations.AddField(
            model_name='bed',
            name='id_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inpatientsystemApp.department'),
        ),
        migrations.AddField(
            model_name='bed',
            name='id_patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inpatientsystemApp.patient'),
        ),
    ]
