# Generated by Django 5.1.5 on 2025-03-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
