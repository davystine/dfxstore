# Generated by Django 5.0.6 on 2024-07-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_item_units_in_stock_alter_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='CF60B9', max_length=50, unique=True),
        ),
    ]
