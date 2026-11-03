[Web 開發](../README.md) › [React](README.md) › React 概覽

# React 概覽 (React Overview)

React 是建構元件式 UI 的 JavaScript **函式庫**：你描述「在某個狀態下畫面應該長怎樣」，React 負責算出要改哪些 DOM 並更新。本篇說明核心原則、函式庫 vs 框架、Virtual DOM 與如何開新專案；瀏覽器與 DOM 的基礎見 [Web 基礎](../web-fundamentals.md)。

## 核心原則

| 原則 | 意義 |
| --- | --- |
| 宣告式 (declarative) | 描述**要什麼**畫面，而不是**怎麼**逐步修改 DOM |
| 元件化 (component-based) | UI 拆成可重用、各自封裝的函式元件 |
| 單向資料流 (unidirectional data flow) | 資料由父元件經 props 往下傳；子元件要改資料時呼叫父元件傳下來的函式 |
| UI = f(state) | 狀態改變 → 元件重新執行 → 產生新的 UI 描述 |

```jsx
function GeneCard({ symbol, chrom }) {          // props 由父元件傳入，唯讀
  return (
    <div className="card">
      <h2>{symbol}</h2>
      <p>Chromosome {chrom}</p>
    </div>
  );
}

function GeneList({ genes }) {
  return genes.map((g) => <GeneCard key={g.id} symbol={g.symbol} chrom={g.chrom} />);  // 清單要給穩定的 key
}
```

| 名詞 | 意義 |
| --- | --- |
| JSX | 在 JavaScript 中寫類似 HTML 的語法，編譯成 `React.createElement` 呼叫；屬性用 `className`、`onClick` |
| props | 父 → 子的輸入，唯讀 |
| state | 元件自己的可變資料，改變會觸發重新渲染，見 [Hooks](hooks.md) |
| `key` | 清單項目的穩定識別（用 ID，不要用陣列索引），讓 React 正確比對新舊清單 |

## 函式庫 vs 框架 (Library vs Framework)

| | 函式庫 (library) | 框架 (framework) |
| --- | --- | --- |
| 控制權 | **你**呼叫函式庫 | **框架**呼叫你的程式碼（控制反轉） |
| 提供 | 可重用的函式或元件 | 完整架構、生命週期、目錄慣例 |
| 自由度 | 高，自己選路由、資料抓取、建置工具 | 低，但決策少、慣例一致 |
| 例子 | React、Lodash、pandas | Next.js、Angular、Django |

React 本身只管 UI；路由、資料抓取、SSR 由框架或其他套件補上：

| 需求 | 常見選擇 |
| --- | --- |
| 全端框架（路由 + SSR / SSG + 資料抓取） | Next.js、React Router（框架模式，前身為 Remix） |
| 純前端路由 | React Router |
| 全域狀態 | Context（內建）、Zustand、Redux Toolkit |
| 伺服器資料快取 | TanStack Query |
| 建置工具 | Vite |

## DOM 與 Virtual DOM

| | DOM | Virtual DOM |
| --- | --- | --- |
| 是什麼 | 瀏覽器中代表 HTML 的樹狀物件 | React 在記憶體中的 UI 描述（一般 JS 物件） |
| 更新成本 | 頻繁直接修改會觸發重新排版、繪製 | 便宜，只是建立新物件 |

```
state 改變 → 元件重新執行 → 新的 Virtual DOM
           → 與舊的比對 (diff / reconciliation) → 算出最小變更 → 只更新那幾個真實 DOM 節點
```

> Virtual DOM 的價值主要在**讓宣告式寫法可行**（每次都「重畫整個 UI 描述」，由 React 找出差異），而不是保證比手寫 DOM 操作快。

## 開新專案

`create-react-app` 已於 2025 年停止維護，不要再用。

| 情境 | 指令 |
| --- | --- |
| 純前端 SPA（儀表板、內部工具） | `npm create vite@latest my-app -- --template react-ts` |
| 需要 SSR / SSG、SEO、全端 | `npx create-next-app@latest my-app` |

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev          # 開發伺服器，預設 http://localhost:5173
npm run build        # 輸出靜態檔到 dist/
```

渲染方式（CSR / SSR / SSG）的差異見 [渲染策略](rendering-strategies.md)。
