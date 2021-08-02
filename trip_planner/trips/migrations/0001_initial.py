# Generated by Django 3.2.5 on 2021-08-02 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='This is the title of your trip.', max_length=100, verbose_name='Trip title')),
                ('start_date', models.DateField(help_text='This is the start date of your trip.', verbose_name='Trip start date')),
                ('end_date', models.DateField(help_text='This is the end date of your trip.', verbose_name='Trip end date')),
                ('notes', models.TextField(blank=True, help_text='These are your notes regarding the trip.', null=True, verbose_name='Trip notes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TripDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('num', models.IntegerField(blank=True, help_text='This shows what day of the trip is this.', null=True, verbose_name='day of the trip')),
                ('date', models.DateField(help_text='This is a date within the trip.', verbose_name='date')),
                ('notes', models.TextField(blank=True, help_text='These are your notes for the day of the trip.', null=True, verbose_name='Day notes')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_days', to='trips.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
