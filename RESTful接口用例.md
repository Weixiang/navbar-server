---
title: NAVBAR
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.23"

---

# NAVBAR

Base URLs:

# Authentication

* API Key (apikey-header-Authorization)
    - Parameter Name: **Authorization**, in: header. 

# Default

## POST MQTT发布

POST /publish

> Body 请求参数

```json
{
  "topic": "nav1044/ping",
  "msg": "est ex esse exercitation commodo"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|Authorization|header|string| 否 |none|
|body|body|object| 否 |none|
|» topic|body|string| 是 |none|
|» msg|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 呼叫设备

POST /calldevice

> Body 请求参数

```json
{
  "sn": "BL748NECGFPW",
  "en": "True",
  "delay": 3
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» sn|body|string| 是 |none|
|» en|body|boolean| 是 |none|
|» delay|body|integer| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 呼叫物品

POST /callitems

> Body 请求参数

```json
{
  "rfid": [
    "F30CHLSVBPAD"
  ],
  "en": true,
  "delay": 51
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» rfid|body|[string]| 是 |none|
|» en|body|boolean| 是 |none|
|» delay|body|integer| 是 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## GET 查找物品

GET /getitems

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|rfid|query|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

## POST 解密数据

POST /encrypt

> Body 请求参数

```json
{
  "payload": "incididunt culpa sit"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» payload|body|string| 是 |none|

> 返回示例

> 200 Response

```json
{
  "result": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» result|string|true|none||none|

# 数据模型

