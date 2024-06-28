
## 成功统一回复

```json
{
  "result": "ok",
  "sender": "server",
  "timestamp": "2024-06-28T11:31:57.021922+08:00"
}
```

## 设备自动发现

```
nav1044/config/H6R8RV8LWSL5
```

```json
{
  "name": "ESP8266-A",
  "sn": "H6R8RV8LWSL5",
  "ip": "192.168.1.101",
  "mac": "00-16-EA-AE-3C-41",
  "sender": "H6R8RV8LWSL5",
  "timestamp": "2024-06-28T11:21:02.105132+08:00"
}
```

## 心跳包

```
nav1044/ping/H6R8RV8LWSL5
```

```json
{
  "msg": "ping",
  "sender": "H6R8RV8LWSL5",
  "timestamp": "2024-06-28T11:21:02.105132+08:00"
}
```

回复

```json
{
  "msg": "pong",
  "sender": "server",
  "timestamp": "2024-06-28T11:35:14.729477+08:00"
}
```

## 上传传感器数据

```
nav1044/sensor/BL748NECGFPW
```

```json
{
  "temp": 29.3,
  "humi": 59.2,
  "light": 141,
  "sender": "BL748NECGFPW",
  "timestamp": "2024-06-28T11:21:02.105132+08:00"
}
```

## 通过设备标签呼叫设备

```
nav1044/reader/H6R8RV8LWSL5
```

```json
{
  "rfid": "U4F6DEQTH4IV",
  "sender": "H6R8RV8LWSL5",
  "timestamp": "2024-06-28T11:21:02.105132+08:00"
}
```