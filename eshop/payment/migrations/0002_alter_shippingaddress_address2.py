# Generated by Django 5.0.6 on 2024-07-17 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
