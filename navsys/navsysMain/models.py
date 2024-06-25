from django.db import models
from django.contrib.auth.models import User

class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    rfid = models.CharField(max_length=100,blank=True, null=True, verbose_name="RFID")
    remark = models.TextField(blank=True, verbose_name="备注")
    class Meta:
        verbose_name_plural = verbose_name = "仓库"
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name="名称")
    rfid = models.CharField(max_length=100,verbose_name="RFID",unique=True)
    price = models.DecimalField(max_digits=10,verbose_name="价格", decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name="数量")
    location = models.ForeignKey(Warehouse,verbose_name="位置", on_delete=models.CASCADE)
    status = models.CharField(max_length=10,verbose_name="状态", choices=[('in', '入库'), ('out', '出库'), ('destroy', '销毁')])
    add_time = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    operator = models.ForeignKey(User,verbose_name="操作员", on_delete=models.CASCADE)
    remark = models.TextField(verbose_name="备注", blank=True)
    class Meta:
        verbose_name_plural = verbose_name = "物品"
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    sn = models.CharField(max_length=100, verbose_name="SN", unique=True)
    location = models.ForeignKey(Warehouse, verbose_name="位置", on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True,verbose_name="IP地址", null=True)
    mac_address = models.CharField(max_length=17, verbose_name="MAC地址", blank=True, null=True)
    last_connection_time = models.DateTimeField(verbose_name="上次活动时间")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name_plural = verbose_name = "设备"
    def __str__(self):
        return self.name

class Environment(models.Model):
    device = models.ForeignKey(Device, verbose_name="设备名", on_delete=models.CASCADE)
    location = models.ForeignKey(Warehouse, verbose_name="位置", on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="温度", blank=True, null=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="湿度", blank=True, null=True)
    light = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="光照", blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    class Meta:
        verbose_name_plural = verbose_name = "环境"
    def __str__(self):
        return f"{self.device.name} - {self.location.name}"

class Record(models.Model):
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="操作员")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="项目名称")
    method = models.CharField(max_length=10, choices=[('in', '入库'), ('out', '出库'), ('destroy', '销毁')], verbose_name="操作")
    remark = models.TextField(blank=True, verbose_name="备注")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    class Meta:
        verbose_name_plural = verbose_name = "记录"
    def __str__(self):
        return f"{self.operator.username} - {self.add_time} - {self.method} - {self.item.name}"


