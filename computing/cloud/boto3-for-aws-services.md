# Boto3 for AWS Services

`boto3` 是 Python 存取 AWS 的官方 SDK。對很多資料工程、自動化與雲端腳本來說，它不是額外工具，而是把 AWS 服務變成程式碼介面的那一層。

這篇筆記的重點不是背所有 API，而是先建立幾個穩定心智模型：

- 用 `client` 呼叫 AWS service API
- 先想清楚 credentials 與 permissions
- 很多 workflow 其實都是 `S3 + 另一個 managed service`

## The Basic Mental Model

最常見的起點長這樣：

```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
response = s3.list_buckets()
```

你可以把它理解成三步：

1. 選一個 AWS service
2. 建立對應的 `client`
3. 呼叫該服務公開的 API method

常見 service name 包括：

- `s3`
- `sns`
- `rekognition`
- `translate`
- `comprehend`

## Credentials Should Not Be Hardcoded

教材裡常直接把 `aws_access_key_id` 和 `aws_secret_access_key` 寫進 `client(...)`，但實務上這通常不是首選。

更穩妥的順序通常是：

1. 本機開發時用 AWS CLI profile 或環境變數
2. 在 EC2、Lambda 或其他 AWS 執行環境中優先用 IAM role
3. 避免把 long-lived secrets 寫死在程式碼或 notebook

例如本機 profile workflow：

```python
import boto3

session = boto3.Session(profile_name="default", region_name="us-east-1")
s3 = session.client("s3")
```

Key point: 能把 credentials 交給 IAM role，就不要自己管理長期 access key。

## Permissions Come Before Code

很多 `boto3` 問題看起來像語法錯誤，其實是權限問題。

例如：

- 你能不能列 bucket
- 你能不能下載某個 object
- 你能不能 publish 到某個 SNS topic
- 你能不能呼叫 Rekognition 或 Translate API

所以 troubleshooting 時，先分清兩件事：

- 程式有沒有呼叫對 API
- 呼叫主體有沒有對應權限

這也就是為什麼 [AWS Security and Cost Management](aws-security-and-cost-management.md) 裡的 least privilege 與 IAM，不只是治理概念，而會直接影響程式是否跑得動。

## S3 as the Default Storage Layer

很多 AWS 自動化腳本都會先碰到 `S3`，因為它很常扮演：

- object storage
- raw landing zone
- 給其他 managed service 讀取的中介層

### List Buckets

```python
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
buckets = s3.list_buckets()
```

這通常只是 sanity check，用來確認：

- credentials 正常
- network 正常
- 你至少有某些 S3 權限

### Download an Object

```python
s3.download_file(
    Bucket="gid-requests",
    Key="potholes.csv",
    Filename="potholes.csv",
)
```

這很適合：

- 把 object 拉回本機或工作節點
- 給 pandas、Spark 或其他處理流程讀取

### Upload an Object

```python
s3.upload_file(
    Filename="report.jpg",
    Bucket="datacamp-img",
    Key="report.jpg",
)
```

心智模型上：

- `Filename` 是本機檔案路徑
- `Bucket` 是目的地 bucket
- `Key` 是 bucket 內的 object 名稱

## SNS for Notifications and Fan-Out

`SNS` 可以先把它理解成託管式 notification / pub-sub 入口。

常見用途：

- 發送 email 或 SMS 通知
- 把事件 fan-out 給多個 subscriber
- 當其他 pipeline 的 alerting 層

基本流程通常是：

1. 建立或取得 topic
2. 建立 subscription
3. publish message

概念範例如下：

```python
import boto3

sns = boto3.client("sns", region_name="us-east-1")

response = sns.publish(
    TopicArn=topic_arn,
    Message="Pipeline finished successfully.",
    Subject="ETL Status",
)
```

Key point: `SNS` 本身不在乎你的業務邏輯，它只負責把 message 往對的 subscription 送出去。

## Rekognition: Managed Vision APIs

`Amazon Rekognition` 提供的是預訓練 vision capabilities，不是完整自訂訓練平台。

它很適合：

- 先快速做 object / label detection
- 從圖片抽文字
- 做 face comparison 或 moderation 類任務

但如果需求是：

- 自訂標籤體系
- 敏感資料不能送出
- 巨量流量下要精細控制成本或模型行為

那就要重新評估是不是應該自己建模型。

### Detect Labels

```python
import boto3

rekog = boto3.client("rekognition", region_name="us-east-1")

response = rekog.detect_labels(
    Image={"S3Object": {"Bucket": "datacamp-img", "Name": "report.jpg"}}
)
```

這類 API 常用來：

- 判斷圖片裡有什麼物件
- 根據標籤做後續篩選或 routing

例如只找特定類別：

```python
for label in response["Labels"]:
    if label["Name"] == "Scooter":
        print("Found scooter")
```

### Detect Text

```python
response = rekog.detect_text(
    Image={"S3Object": {"Bucket": "datacamp-img", "Name": "street-sign.jpg"}}
)
```

這種 pattern 適合：

- 路牌或招牌文字抽取
- 文件影像中的簡單 OCR-like workflow

### Compare Faces

```python
response = rekog.compare_faces(
    SourceImage={"S3Object": {"Bucket": "datacamp-img", "Name": "source.jpg"}},
    TargetImage={"S3Object": {"Bucket": "datacamp-img", "Name": "target.jpg"}},
)
```

這類 API 很方便，但也更容易碰到：

- 隱私問題
- 誤判風險
- 合規與安全需求

所以功能可用，不代表任何場景都適合直接上。

## Translate for Quick Multilingual Output

`Amazon Translate` 適合把既有文字快速轉成其他語言，不需要自己訓練模型。

```python
import boto3

translate = boto3.client("translate", region_name="us-east-1")

resp = translate.translate_text(
    Text="Hello, how are you?",
    SourceLanguageCode="en",
    TargetLanguageCode="es",
)

translated = resp["TranslatedText"]
```

這很適合：

- 多語系 UI 文案原型
- 事件描述先快速翻譯
- 跨語言資料前處理

但也要記得：

- 翻譯品質會隨語境變動
- 專業術語不一定可靠
- 高敏感內容要先考慮資料治理

## Comprehend for Managed NLP

`Amazon Comprehend` 提供的是文字層級的 managed NLP API。

這門課裡最實用的兩個入口是：

- language detection
- sentiment detection

### Detect Dominant Language

```python
import boto3

comprehend = boto3.client("comprehend", region_name="us-east-1")

response = comprehend.detect_dominant_language(
    Text="Hay basura por todas partes a lo largo de la carretera."
)
```

這很適合在 multilingual text pipeline 裡當第一步，先決定後面要不要翻譯。

### Detect Sentiment

```python
response = comprehend.detect_sentiment(
    Text="Maksim is amazing.",
    LanguageCode="en",
)
```

適合：

- 簡單 feedback triage
- social / support text 的初步分類
- 先做規則式 routing，再決定是否需要更重的模型

## A Common AWS Pattern: S3 + Managed Service + Tabular Output

這門課背後其實一直重複同一種結構：

1. 把檔案放到 `S3`
2. 呼叫某個 managed service
3. 把回傳結果整理進 dataframe、CSV 或 downstream workflow

例如：

- `S3 -> Rekognition -> labels`
- `S3 -> Rekognition -> text`
- `raw text -> Translate -> translated text`
- `raw text -> Comprehend -> sentiment`

Key point: 很多 AWS 自動化工作的價值，不在於自己重新實作模型，而在於把 service 組裝成可維運的 pipeline。

## Choosing Managed APIs vs Building Your Own

可以先用這個簡化判斷：

- 要快速可用、程式簡單、需求通用：先考慮 managed API
- 要高度客製、資料敏感、量非常大：再考慮自己建模型或自管系統

這跟 [AWS Services Overview](aws-services-overview.md) 裡提到的 AI / ML services 心智模型一致：不是每個 AI 任務都要從頭訓練。

## Practical Reminders

- 先確認 region、credentials、permissions，再檢查程式碼。
- `boto3` 最常見的資料交換形式是 Python dict，讀回應時要習慣查 key 結構。
- `S3` 很常是其他 AWS AI / notification service 的資料入口。
- 在 production 中，優先用 IAM roles，不要把 secret 寫進 repo。
- managed service 可以大幅加快原型，但不會自動幫你解決隱私、成本與誤判風險。

## Related Concepts

- [AWS Services Overview](aws-services-overview.md)
- [AWS Security and Cost Management](aws-security-and-cost-management.md)
- [AWS Streaming with Kinesis and Lambda](../../data-science/data-engineering/aws-streaming-with-kinesis-and-lambda.md)
- [API and HTTP in Python](../../data-science/python-foundations/api-http.md)

[Back to Cloud](README.md)
