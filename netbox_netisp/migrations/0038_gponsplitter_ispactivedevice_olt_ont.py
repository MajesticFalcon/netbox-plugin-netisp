# Generated by Django 3.2 on 2021-04-24 04:11

from django.db import migrations, models
import django.db.models.deletion
import ipam.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dcim', '0130_sitegroup'),
        ('netbox_netisp', '0037_alter_attachment_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISPActiveDevice',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField(blank=True, null=True)),
                ('ip_address', ipam.fields.IPAddressField(blank=True, default='', null=True)),
                ('uuid', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dcim.devicetype')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dcim.manufacturer')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dcim.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OLT',
            fields=[
                ('ispactivedevice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netbox_netisp.ispactivedevice')),
            ],
            options={
                'abstract': False,
            },
            bases=('netbox_netisp.ispactivedevice',),
        ),
        migrations.CreateModel(
            name='GPONSplitter',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('uplink_type', models.CharField(max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ONT',
            fields=[
                ('ispactivedevice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netbox_netisp.ispactivedevice')),
                ('uplink', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='netbox_netisp.gponsplitter')),
            ],
            options={
                'abstract': False,
            },
            bases=('netbox_netisp.ispactivedevice',),
        ),
    ]
