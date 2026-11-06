[Web 開發](../README.md) › [React](README.md) › 渲染策略

# 渲染策略 (Rendering Strategies)

渲染 (rendering) 是把應用程式碼變成使用者看到的 HTML。差別在於 HTML **在哪裡、什麼時候**產生：瀏覽器執行時、每次請求時在伺服器、或建置時一次產生。選擇會影響首次載入速度、SEO、伺服器成本與資料新鮮度。

## 比較

| 策略 | HTML 何時、在哪產生 | 首次載入 | SEO | 伺服器負擔 | 資料新鮮度 | 適合 |
| --- | --- | --- | --- | --- | --- | --- |
| CSR (Client-Side Rendering) | 瀏覽器下載 JS 後執行產生 | 慢：先收到幾乎空的 HTML | 差（依賴爬蟲執行 JS） | 低：只送靜態檔 | 即時（前端呼叫 API） | 登入後的 dashboard、內部工具 |
| SSR (Server-Side Rendering) | **每次請求**在伺服器產生 | 快：直接收到完整 HTML | 好 | 高 | 每次請求都最新 | 個人化頁面、經常變動且要 SEO |
| SSG (Static Site Generation) | **建置時**產生一次 | 最快：可放 CDN | 好 | 幾乎無 | 到下次建置前不變 | 文件、部落格、行銷頁 |
| ISR (Incremental Static Regeneration) | 建置時產生，之後依設定時間在背景重新產生 | 快 | 好 | 低 | 延遲一段時間 | 商品頁、大量但不常變的頁面 |

```text
CSR:  請求 → 空 HTML + JS ─────────► 下載執行 JS ─► 呼叫 API ─► 畫面
SSR:  請求 → 伺服器取資料、產生 HTML ─► 完整畫面（尚不可互動）─► hydration ─► 可互動
SSG:  建置時產生 HTML ── 請求 → CDN 直接回傳 ─► 完整畫面 ─► hydration ─► 可互動
```

## Hydration

SSR / SSG 送出的 HTML 只能看、不能互動；瀏覽器載入 JS 後，React 把事件處理與狀態「接上」既有的 HTML，這步稱為 hydration。

| 注意 | 說明 |
| --- | --- |
| 伺服器與瀏覽器渲染結果要一致 | 用 `Date.now()`、`Math.random()`、`window` 產生內容會造成 hydration mismatch 警告 |
| 可看到但還不能點 | JS 很大時，畫面出現到可互動之間有空窗 |
| React Server Components | Next.js App Router 的預設：元件在伺服器執行、不送 JS 到瀏覽器，只有標記 `"use client"` 的元件需要 hydration |

## SEO

| 情況 | 搜尋引擎看到 |
| --- | --- |
| SSR / SSG | 完整 HTML，內容與 `<title>`、`<meta>` 直接可讀 |
| CSR | 初始 HTML 幾乎是空的 `<div id="root">`；Google 會執行 JS 但較慢、不保證，其他爬蟲與社群預覽（連結縮圖）常看不到 |

CSR 應用需要 SEO 時，改用 Next.js 的 SSR / SSG，或對公開頁面預先渲染 (prerendering)。登入後才看得到的頁面不需要 SEO，CSR 即可。

## 怎麼選

```text
需要 SEO 或連結預覽？
├─ 否 → CSR（Vite + React）
└─ 是 → 內容每個使用者 / 每次請求都不同？
        ├─ 是 → SSR
        └─ 否 → 多久變一次？
                ├─ 幾乎不變 → SSG
                └─ 定期變動、頁面很多 → ISR
```

同一個 Next.js 專案可以逐頁選擇策略。
