# Generated by Django 4.2.2 on 2023-06-18 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10, null=True)),
                ('release_date', models.DateField(null=True)),
                ('capsule_image', models.TextField(default="{% static 'header_image.jpg' %}")),
                ('header_image', models.TextField(default="{% static 'header_image.jpg' %}")),
                ('is_free', models.BooleanField(null=True)),
                ('initial_price', models.IntegerField(null=True)),
                ('discount_percent', models.IntegerField(null=True)),
                ('final_price', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'app',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('rank', models.IntegerField(primary_key=True, serialize=False)),
                ('last_week_rank', models.IntegerField()),
                ('peak_in_game', models.IntegerField()),
                ('app', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rank', to='app.app')),
            ],
            options={
                'db_table': 'rank',
            },
        ),
    ]
