# Generated by Django 3.1.3 on 2021-02-28 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netisp', '0015_auto_20210228_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntennaProfile',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netbox_netisp.equipment')),
                ('azimuth', models.CharField(max_length=30)),
                ('beamwidth', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('netbox_netisp.equipment',),
        ),
        migrations.CreateModel(
            name='RadioAccessPoint',
            fields=[
                ('equipment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netbox_netisp.equipment')),
                ('frequency', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('antenna', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netbox_netisp.antennaprofile')),
            ],
            options={
                'abstract': False,
            },
            bases=('netbox_netisp.equipment',),
        ),
    ]