# Generated by Django 3.2.7 on 2021-11-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_client_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='DOB'),
        ),
    ]