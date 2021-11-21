# Generated by Django 3.2.7 on 2021-11-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_licenseissue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='licenses',
        ),
        migrations.AddField(
            model_name='licenseissue',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]