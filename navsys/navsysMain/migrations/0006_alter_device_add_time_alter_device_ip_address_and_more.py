# Generated by Django 5.0.6 on 2024-06-23 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("navsysMain", "0005_item_rfid_warehouse_rfid"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="add_time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="添加时间"),
        ),
        migrations.AlterField(
            model_name="device",
            name="ip_address",
            field=models.GenericIPAddressField(
                blank=True, null=True, verbose_name="IP地址"
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="last_connection_time",
            field=models.DateTimeField(verbose_name="上次活动时间"),
        ),
        migrations.AlterField(
            model_name="device",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="navsysMain.warehouse",
                verbose_name="位置",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="mac_address",
            field=models.CharField(
                blank=True, max_length=17, null=True, verbose_name="MAC地址"
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="name",
            field=models.CharField(max_length=100, verbose_name="名称"),
        ),
        migrations.AlterField(
            model_name="device",
            name="sn",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="SN"
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="add_time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="时间"),
        ),
        migrations.AlterField(
            model_name="environment",
            name="device",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="navsysMain.device",
                verbose_name="设备名",
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="humidity",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="湿度"
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="light",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="光照"
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="navsysMain.warehouse",
                verbose_name="位置",
            ),
        ),
        migrations.AlterField(
            model_name="environment",
            name="temperature",
            field=models.DecimalField(
                decimal_places=2, max_digits=5, verbose_name="温度"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="add_time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="添加时间"),
        ),
        migrations.AlterField(
            model_name="item",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="navsysMain.warehouse",
                verbose_name="位置",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(max_length=100, verbose_name="名称"),
        ),
        migrations.AlterField(
            model_name="item",
            name="operator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="操作员",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="价格"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="quantity",
            field=models.PositiveIntegerField(verbose_name="数量"),
        ),
        migrations.AlterField(
            model_name="item",
            name="remark",
            field=models.TextField(blank=True, verbose_name="备注"),
        ),
        migrations.AlterField(
            model_name="item",
            name="rfid",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="RFID"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="status",
            field=models.CharField(
                choices=[("in", "入库"), ("out", "出库"), ("destroy", "销毁")],
                max_length=10,
                verbose_name="状态",
            ),
        ),
        migrations.AlterField(
            model_name="record",
            name="add_time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="时间"),
        ),
        migrations.AlterField(
            model_name="record",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="navsysMain.item",
                verbose_name="项目名称",
            ),
        ),
        migrations.AlterField(
            model_name="record",
            name="method",
            field=models.CharField(
                choices=[("in", "入库"), ("out", "出库"), ("destroy", "销毁")],
                max_length=10,
                verbose_name="操作",
            ),
        ),
        migrations.AlterField(
            model_name="record",
            name="operator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="操作员",
            ),
        ),
        migrations.AlterField(
            model_name="record",
            name="remark",
            field=models.TextField(blank=True, verbose_name="备注"),
        ),
    ]
