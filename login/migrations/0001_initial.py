# Generated by Django 3.0.5 on 2025-03-12 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginStudent',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('emailid', models.CharField(max_length=100, unique=True)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('dept', models.CharField(max_length=6)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TeacherAdmin',
            fields=[
                ('staffid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('usertype', models.CharField(choices=[('teacher', 'Teacher'), ('admin', 'Admin')], max_length=10)),
                ('emailid', models.EmailField(max_length=254, unique=True)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('dept', models.CharField(max_length=6)),
            ],
        ),
    ]
