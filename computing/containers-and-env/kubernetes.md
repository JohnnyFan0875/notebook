[Computing](../README.md) › [容器與環境](README.md) › Kubernetes

# Kubernetes

Kubernetes（K8s）是容器編排平台：在一群機器（叢集）上排程、擴展、修復、更新容器化的應用。應用拆成多個服務、需要跨機器協調運行時才需要它；單機跑幾個容器用 [Docker Compose](docker/compose.md) 就夠，批次分析用 HPC 排程器。雲端有託管版本（EKS、AKS、GKE），不必自己架控制平面。

| 目標 | Kubernetes 怎麼做 |
| --- | --- |
| 排程 | 把 Pod 放到有足夠資源的節點 |
| 自我修復 | 容器或節點掛掉，自動重建 |
| 擴展 | 增減副本數；可依 CPU 自動調整（HPA） |
| 對外服務 | Service、Ingress 提供穩定的位址 |
| 更新 | 滾動更新，失敗可回滾 |

## 架構

```text
Cluster
├── Control plane：API server、scheduler、controller manager、etcd（叢集狀態）
└── Nodes（工作機器）
    └── Pod（最小部署單位，通常一個主要容器；有自己的叢集內 IP，可被取代）
```

你用 YAML 宣告**想要的狀態**（「跑 3 個 nginx 副本」），控制器持續讓實際狀態符合宣告。

## 主要物件

| 物件 | 用途 |
| --- | --- |
| Pod | 一或多個共用網路與儲存的容器；短暫、可替換 |
| Deployment | 管理無狀態應用的副本數與滾動更新 |
| StatefulSet | 有狀態應用（資料庫）：穩定的名稱（`db-0`、`db-1`）與各自的儲存，依序建立 |
| Job / CronJob | 跑完就結束的批次工作 / 定時工作 |
| Service | 依 label 選取一組 Pod，提供穩定的位址與負載平衡 |
| Ingress | 外部 HTTP(S) 流量依網域 / 路徑路由到 Service |
| ConfigMap / Secret | 設定與機密，以環境變數或檔案注入 |
| PersistentVolumeClaim (PVC) | 申請儲存空間；由 StorageClass 動態配置 PersistentVolume (PV) |
| Namespace | 叢集內的邏輯分區（團隊、環境） |

```yaml
# deployment.yaml：3 個 nginx 副本 + 對內的 Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }            # Service 依這個 label 找到 Pod
    spec:
      containers:
        - name: web
          image: nginx:1.27           # 固定版本，不用 latest
          ports: [{ containerPort: 80 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }   # 排程依據
            limits:   { cpu: 500m, memory: 256Mi }   # 超過記憶體上限會被 OOMKilled
      nodeSelector:
        disktype: ssd                 # 只排到有此 label 的節點
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector: { app: web }
  ports: [{ port: 80, targetPort: 80 }]
```

## kubectl

```bash
kubectl apply -f deployment.yaml            # 建立或更新（宣告式，建議）
kubectl get pods -o wide                    # 列出 Pod 與所在節點
kubectl get deploy,svc,pvc                  # 多種資源
kubectl describe pod <name>                 # 詳細狀態與事件（除錯第一步）
kubectl logs -f <pod>                       # 看 log
kubectl exec -it <pod> -- bash              # 進入容器
kubectl scale deployment web --replicas=5
kubectl rollout status deployment/web       # 更新進度
kubectl rollout undo deployment/web         # 回滾
kubectl port-forward svc/web 8080:80        # 本機 8080 → Service，除錯用
kubectl delete -f deployment.yaml
kubectl get sc; kubectl get pv; kubectl get pvc   # 儲存
```

| Pod 狀態 | 常見原因 |
| --- | --- |
| `Pending` | 資源不足、PVC 無法配置、nodeSelector 沒有符合的節點 |
| `ImagePullBackOff` | 映像檔名稱 / tag 錯誤、私有 registry 沒設認證 |
| `CrashLoopBackOff` | 容器啟動後立刻結束：看 `kubectl logs --previous` |
| `OOMKilled` | 超過記憶體 limit |

> 資料與 ML 情境：Kubeflow、Argo Workflows 在 Kubernetes 上跑 ML pipeline；Nextflow 也能以 Kubernetes 作為 executor。模型服務的部署見 [部署與監控](../../data-science/machine-learning/production/deployment-and-monitoring.md)。
