# Generated by Django 3.1.5 on 2021-01-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]