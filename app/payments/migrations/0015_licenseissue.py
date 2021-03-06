# Generated by Django 3.2.7 on 2021-11-21 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_payment_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.client')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.license')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.year')),
            ],
        ),
    ]
