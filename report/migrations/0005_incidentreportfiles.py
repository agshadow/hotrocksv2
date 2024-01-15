# Generated by Django 5.0 on 2024-01-04 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_alter_incidentreport_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentReportFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('incident_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.incidentreport')),
            ],
        ),
    ]