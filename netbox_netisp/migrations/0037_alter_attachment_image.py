# Generated by Django 3.2 on 2021-04-23 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netisp', '0036_auto_20210423_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='image',
            field=models.ImageField(upload_to='netbox_netisp/attachments/'),
        ),
    ]
