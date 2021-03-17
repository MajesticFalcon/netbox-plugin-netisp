# Generated by Django 3.1.3 on 2021-03-15 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netisp', '0020_employee_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='date_closed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_opened',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
