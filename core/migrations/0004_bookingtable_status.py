# Generated by Django 5.1.2 on 2024-12-04 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_bookingtable_booking_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingtable',
            name='status',
            field=models.IntegerField(choices=[(0, 'In Progress'), (1, 'Approved')], null=True),
        ),
    ]
