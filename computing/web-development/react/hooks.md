[Web 開發](../README.md) › [React](README.md) › Hooks

# React Hooks

Hooks 讓函式元件擁有狀態、副作用與其他 React 功能（不必寫 class 元件）。名稱以 `use` 開頭，只能在元件或自訂 Hook 的**最上層**呼叫。

## 常用 Hooks

| Hook | 用途 | 觸發重新渲染？ |
| --- | --- | --- |
| `useState` | 元件內的狀態 | 是（值改變時） |
| `useEffect` | 副作用：呼叫 API、訂閱事件、計時器、同步外部系統 | — |
| `useRef` | 跨渲染保存值、取得 DOM 節點 | **否** |
| `useContext` | 讀取上層提供的 Context（主題、登入使用者） | 是（Context 值改變時） |
| `useMemo` | 快取昂貴計算的結果 | — |
| `useCallback` | 快取函式參照（傳給 memo 子元件時） | — |
| `useReducer` | 多個相關狀態、更新邏輯複雜時取代 `useState` | 是 |

## `useState`

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return (
    <>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount((c) => c + 1)}>+1（函式更新）</button>
      <p>{count}</p>
    </>
  );
}
```

| 規則 | 說明 |
| --- | --- |
| 狀態更新是非同步、批次的 | `setCount(count + 1)` 連呼叫兩次只加 1；依舊值計算時用函式形式 `setCount(c => c + 1)` |
| 不要直接修改物件 / 陣列 | `list.push(x)` 不會觸發渲染；用新物件：`setList([...list, x])`、`setObj({ ...obj, k: v })` |
| 能算出來的就不要存成 state | 篩選後的清單、總數直接在渲染時算 |

## `useEffect` 與 dependency array

`useEffect(fn, deps)` 在渲染**之後**執行 `fn`；第二個參數決定何時重跑。

| `deps` | 何時執行 |
| --- | --- |
| 省略 | **每次**渲染後（很少是你要的） |
| `[]` | 只在元件掛載 (mount) 後執行一次 |
| `[a, b]` | 掛載後，以及 `a` 或 `b` 改變後 |

回傳的函式是清理函式 (cleanup)：在下次 effect 執行前與元件卸載 (unmount) 時呼叫。

```jsx
import { useEffect, useState } from "react";

function Gene({ symbol }) {
  const [gene, setGene] = useState(null);

  useEffect(() => {
    const ctrl = new AbortController();                       // 1. symbol 改變時取消舊請求
    fetch(`https://rest.ensembl.org/lookup/symbol/homo_sapiens/${symbol}?content-type=application/json`,
          { signal: ctrl.signal })
      .then((r) => r.json())
      .then(setGene)
      .catch((e) => { if (e.name !== "AbortError") console.error(e); });
    return () => ctrl.abort();                                // 2. cleanup
  }, [symbol]);                                               // 3. 只在 symbol 改變時重抓

  useEffect(() => {
    document.title = gene ? gene.display_name : "Loading";   // 同步外部系統（文件標題）
  }, [gene]);

  return <p>{gene ? gene.id : "Loading…"}</p>;
}
```

> React 18+ 的開發模式 (Strict Mode) 會刻意讓 effect 執行 → 清理 → 再執行一次，用來暴露沒寫 cleanup 的 bug；正式環境只跑一次。

## `useRef`

```jsx
import { useRef } from "react";

function SearchBox() {
  const inputRef = useRef(null);        // 1. 取得 DOM 節點
  const clicks = useRef(0);             // 2. 跨渲染保存值，改變不觸發渲染
  return (
    <>
      <input ref={inputRef} />
      <button onClick={() => { clicks.current += 1; inputRef.current.focus(); }}>Focus</button>
    </>
  );
}
```

| `useState` | `useRef` |
| --- | --- |
| 值改變 → 重新渲染 | 改 `.current` 不會渲染 |
| 畫面上要顯示的資料 | 計時器 ID、前一次的值、DOM 節點 |

## 常見錯誤

| 錯誤 | 症狀 | 修正 |
| --- | --- | --- |
| 在 `if`、迴圈、巢狀函式內呼叫 Hook | 錯誤：Hooks 順序改變 | 只在最上層呼叫；條件寫在 Hook 內部 |
| effect 裡 `setState` 且沒有 deps | 無限渲染迴圈 | 加正確的 dependency array |
| deps 漏掉 effect 中用到的變數 | 讀到舊值（stale closure） | 依 ESLint `react-hooks/exhaustive-deps` 補齊 |
| deps 放每次渲染都新建的物件 / 函式 | effect 每次都重跑 | 移進 effect 內、或用 `useMemo` / `useCallback` |
| 用 effect 計算衍生資料 | 多一次渲染、狀態不同步 | 直接在渲染時計算，昂貴時用 `useMemo` |
| 沒有 cleanup 的訂閱 / 計時器 | 記憶體洩漏、卸載後仍 setState | 回傳清理函式 |
| 快速切換時舊請求晚回來覆蓋新結果 | 畫面顯示錯的資料 | `AbortController` 或忽略旗標；或改用 TanStack Query |

> 抓伺服器資料時，實務上多用 TanStack Query 或框架（Next.js）的資料抓取，它們處理了快取、重試、競態，比手寫 `useEffect` 可靠。
