# Generated by Django 4.2.3 on 2023-07-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number_or_title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]