# Generated by Django 3.1.3 on 2021-02-28 00:50

from django.db import migrations, models
import django.db.models.deletion
import ipam.fields


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netisp', '0013_equipment_device_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPremiseEquipment',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netbox_netisp.equipment')),
                ('ip_address', ipam.fields.IPNetworkField()),
            ],
            options={
                'abstract': False,
            },
            bases=('netbox_netisp.equipment',),
        ),
    ]
