# Generated by Django 3.1.4 on 2020-12-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getcurrencyrate', '0003_auto_20201224_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=15),
        ),
    ]
