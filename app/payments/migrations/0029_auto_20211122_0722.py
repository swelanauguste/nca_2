# Generated by Django 3.2.7 on 2021-11-22 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0028_rename_license_item_licensepayment_issued_license'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='year',
            options={'ordering': ('year',)},
        ),
        migrations.AddField(
            model_name='year',
            name='slug',
            field=models.SlugField(blank=True, max_length=4, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='year',
            name='year',
            field=models.IntegerField(max_length=4, unique=True),
        ),
    ]
