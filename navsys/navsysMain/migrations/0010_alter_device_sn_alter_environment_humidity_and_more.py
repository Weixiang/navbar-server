# Generated by Django 5.0.6 on 2024-06-24 03:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("navsysMain", "0009_alter_warehouse_name_alter_warehouse_remark_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="sn",
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=100,
                unique=True,
                verbose_name="SN",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="environment",
            name="humidity",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="湿度"
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="light",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="光照"
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="temperature",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True, verbose_name="温度"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="rfid",
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=100,
                unique=True,
                verbose_name="RFID",
            ),
            preserve_default=False,
        ),
    ]
