# Generated by Django 5.0 on 2024-01-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_incidentreportfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentreportfiles',
            name='filename',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
