# Generated by Django 4.1 on 2022-09-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gold', models.IntegerField()),
                ('silver', models.IntegerField()),
                ('bronze', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
    ]
