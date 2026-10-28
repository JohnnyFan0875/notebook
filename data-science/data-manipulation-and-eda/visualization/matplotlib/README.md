[資料處理與 EDA](../../README.md) › [視覺化](../README.md) › Matplotlib

# Matplotlib

Python 最底層也最完整的繪圖套件：Seaborn 與 pandas `.plot()` 都畫在 Matplotlib 的 `Axes` 上，所以要調細節、組多子圖或輸出出版級圖時都會回到這裡。本章以 Matplotlib 3.10+ 為準。

```text
基礎（figure / axes / 輸出）→ 折線、散布 → 長條、直方、箱型 → 雙軸與註解
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [基礎](basics.md) | `fig, ax`、標籤、刻度、log 軸、樣式、存檔、中文字型 | 圖的骨架怎麼建、怎麼輸出？ |
| [折線圖](line-plot.md) | 多條線、子圖、誤差線、參考線 | 怎麼畫趨勢與不確定性？ |
| [散布圖](scatter-plot.md) | 分組、顏色 / 大小編碼、趨勢線、overplotting | 兩個連續變數什麼關係？點太多怎麼辦？ |
| [長條圖與直方圖](bar-histogram.md) | 分組 / 堆疊長條、直方圖、bins | 類別怎麼比較？分布長怎樣？ |
| [箱型圖](box-plot.md) | 鬚的定義、分組、notch、疊加原始點 | 各組分布與離群值？ |
| [進階：雙軸與註解](advanced.md) | `twinx`、`annotate`、`axvspan` | 怎麼標出重點、比較不同尺度？ |

## 兩種寫法

| | 物件導向 (OO) | pyplot (狀態式) |
| --- | --- | --- |
| 寫法 | `fig, ax = plt.subplots()`；`ax.plot()`、`ax.set_title()` | `plt.plot()`、`plt.title()` |
| 作用對象 | 明確指定哪個 axes | 「目前的」figure / axes |
| 建議 | 多子圖、函式、正式腳本都用這個 | 互動中快速看一眼 |

> 本章範例都用 OO 寫法。Seaborn 的 axes-level 函式接受 `ax=`，pandas `.plot()` 回傳 `ax`，都能接著用 `ax.set_*()` 調整。

| 相關 | 連結 |
| --- | --- |
| 統計圖（自動分組、CI） | [Seaborn](../seaborn/README.md) |
| 從 DataFrame 快速畫 | [pandas Plotting](../pandas-plotting.md) |
| 選圖與避免誤導 | [圖表設計原則](../chart-design-principles.md) |
