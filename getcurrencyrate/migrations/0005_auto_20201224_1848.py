# Generated by Django 3.1.4 on 2020-12-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getcurrencyrate', '0004_auto_20201224_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]
