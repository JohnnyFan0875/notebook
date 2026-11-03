[Computing](../README.md) › [Cloud](README.md) › Boto3

# Boto3：用 Python 操作 AWS (Boto3 for AWS Services)

`boto3` 是 AWS 官方的 Python SDK，把 AWS 服務變成程式介面，用於資料工程、自動化與雲端腳本。心智模型：**選服務 → 建立 client → 呼叫 API 方法 → 讀回傳的 dict**；很多工作流其實就是「S3 + 另一個託管服務」。服務本身見 [AWS 服務總覽](aws-services-overview.md)。

## 認證：不要把金鑰寫在程式裡

boto3 依序在這些地方找憑證（找到就停）：

| 順序 | 來源 | 用在 |
| --- | --- | --- |
| 1 | 程式中傳入的參數 | **避免** |
| 2 | 環境變數 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` | CI、容器 |
| 3 | `~/.aws/credentials`、`~/.aws/config` 的 profile（`aws configure`、`aws sso login` 產生） | 本機開發 |
| 4 | EC2 / ECS / Lambda 的 IAM role | **在 AWS 上執行時的首選** |

```python
import boto3

# 本機：用 profile（SSO 或 aws configure 設定）
session = boto3.Session(profile_name="lab", region_name="us-east-1")
s3 = session.client("s3")

# 在 EC2 / Lambda 上：自動使用 IAM role，不必任何設定
s3 = boto3.client("s3", region_name="us-east-1")
```

> 很多 boto3 錯誤看似程式問題，其實是權限問題（`AccessDenied`）或區域錯誤。除錯時先分清楚：API 呼叫對不對？呼叫者有沒有權限？區域對不對？權限設計見 [AWS 安全與成本管理](aws-security-and-cost-management.md)。

## S3

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3", region_name="us-east-1")

s3.list_buckets()["Buckets"]                                    # 檢查憑證與權限的 sanity check

s3.upload_file(Filename="report.html", Bucket="my-lab-results", Key="2024/report.html")
s3.download_file(Bucket="my-lab-data", Key="raw/sample.csv", Filename="sample.csv")

# 列出物件：一次最多回傳 1000 筆，要用 paginator
paginator = s3.get_paginator("list_objects_v2")
keys = [obj["Key"]
        for page in paginator.paginate(Bucket="my-lab-data", Prefix="fastq/")
        for obj in page.get("Contents", [])]

# 產生暫時的下載連結（不必公開 bucket）
url = s3.generate_presigned_url("get_object",
                                Params={"Bucket": "my-lab-results", "Key": "2024/report.html"},
                                ExpiresIn=3600)

try:
    s3.head_object(Bucket="my-lab-data", Key="raw/missing.csv")
except ClientError as e:
    print(e.response["Error"]["Code"])                          # '404'、'403'
```

| 參數 | 意義 |
| --- | --- |
| `Bucket` | bucket 名稱 |
| `Key` | 物件在 bucket 內的完整名稱（`2024/report.html`）；S3 沒有真正的資料夾，`/` 只是名稱的一部分 |
| `Filename` | 本機路徑 |

pandas 可直接讀寫 S3（需安裝 `s3fs`）：`pd.read_csv("s3://my-lab-data/raw/sample.csv")`。大量檔案同步用 AWS CLI：`aws s3 sync ./results s3://my-lab-results/run1/`。

## SNS：通知

```python
sns = boto3.client("sns", region_name="us-east-1")
topic_arn = sns.create_topic(Name="pipeline-status")["TopicArn"]       # 已存在時回傳同一個 ARN
sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint="me@example.com")   # 需到信箱確認
sns.publish(TopicArn=topic_arn, Subject="ETL Status", Message="Pipeline finished successfully.")
```

SNS 是 pub/sub：把訊息送給所有訂閱者（email、SMS、Lambda、SQS），不關心業務邏輯。常用於 pipeline 完成或失敗通知。

## 預訓練 AI 服務

```python
# Rekognition：影像分析（圖片在 S3 上）
rekog = boto3.client("rekognition", region_name="us-east-1")
img = {"S3Object": {"Bucket": "my-images", "Name": "street.jpg"}}
labels = rekog.detect_labels(Image=img, MaxLabels=10, MinConfidence=80)["Labels"]
[l["Name"] for l in labels]                                     # ['Road', 'Car', ...]
texts = rekog.detect_text(Image=img)["TextDetections"]          # 路牌、招牌文字
rekog.compare_faces(SourceImage=img, TargetImage={"S3Object": {"Bucket": "my-images", "Name": "b.jpg"}})

# Translate：翻譯
translate = boto3.client("translate", region_name="us-east-1")
translate.translate_text(Text="Hello, how are you?",
                         SourceLanguageCode="en", TargetLanguageCode="es")["TranslatedText"]

# Comprehend：語言偵測、情緒分析
comprehend = boto3.client("comprehend", region_name="us-east-1")
comprehend.detect_dominant_language(Text="Hay basura por todas partes.")["Languages"][0]["LanguageCode"]   # 'es'
comprehend.detect_sentiment(Text="The new pipeline is amazing.", LanguageCode="en")["Sentiment"]          # 'POSITIVE'
```

常見組合：`S3 → Rekognition → 標籤表`、`原始文字 → Comprehend 偵測語言 → Translate → Comprehend 情緒 → DataFrame`。把回傳的 dict 整理成表格：`pd.DataFrame(labels)`。

| 先用託管 API | 考慮自建模型 |
| --- | --- |
| 需求通用、要快速可用 | 需要自訂標籤體系 |
| 量不大 | 量很大，按次計費變貴 |
| 資料可以送出 | 敏感資料（病歷、可識別的人臉）不能送到外部服務 |

> 人臉比對、情緒分析等 API 好用，但有隱私、誤判與偏誤問題；功能可用不代表適合任何場景，見 [Responsible AI](../../data-science/responsible-ai/README.md)。

## 實務守則

| 守則 | 說明 |
| --- | --- |
| 先確認區域、憑證、權限 | 多數錯誤來自這三者 |
| 回應是巢狀 dict | 先 `print` 或查官方文件確認 key 結構 |
| 列表類 API 用 paginator | 否則只拿到第一頁 |
| 捕捉 `ClientError` | 依 `e.response["Error"]["Code"]` 處理 |
| 正式環境用 IAM role | 不在 repo、notebook 中放金鑰 |

呼叫一般 HTTP API 的寫法見 [API 與 HTTP](../../data-science/python-foundations/api-http.md)。
