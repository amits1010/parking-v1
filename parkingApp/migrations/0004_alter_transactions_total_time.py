# Generated by Django 4.2.6 on 2023-11-02 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkingApp', '0003_alter_reservations_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='total_time',
            field=models.CharField(max_length=200),
        ),
    ]
