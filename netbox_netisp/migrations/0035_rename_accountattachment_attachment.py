# Generated by Django 3.2 on 2021-04-23 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netisp', '0034_accountattachment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountAttachment',
            new_name='Attachment',
        ),
    ]
