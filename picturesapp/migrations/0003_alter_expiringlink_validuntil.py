# Generated by Django 4.1.7 on 2023-03-04 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picturesapp', '0002_alter_picture_uploaded_expiringlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='validuntil',
            field=models.IntegerField(),
        ),
    ]
