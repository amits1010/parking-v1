# Generated by Django 4.2.6 on 2023-11-02 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wheeler', models.CharField(max_length=50)),
                ('rate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.TimeField()),
                ('payment', models.CharField(choices=[('1', 'pending'), ('2', 'paid')], default='1', max_length=10)),
                ('garage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingApp.garage')),
            ],
        ),
        migrations.CreateModel(
            name='vehicies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license', models.CharField(max_length=50)),
                ('vehicle_type', models.CharField(choices=[('1', 'Two wheeler'), ('2', 'Four Wheeler')], default='1', max_length=30)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_time', models.CharField(max_length=10)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reservation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingApp.reservations')),
            ],
        ),
        migrations.CreateModel(
            name='spots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(choices=[('1', 'Two wheeler'), ('2', 'Four Wheeler')], default='1', max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('garage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingApp.garage')),
            ],
        ),
        migrations.AddField(
            model_name='reservations',
            name='spot_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingApp.spots'),
        ),
        migrations.AddField(
            model_name='garage',
            name='rate_four_wheeler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='four_wheeler', to='parkingApp.rate'),
        ),
        migrations.AddField(
            model_name='garage',
            name='rate_two_wheeler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='two_wheeler', to='parkingApp.rate'),
        ),
    ]
