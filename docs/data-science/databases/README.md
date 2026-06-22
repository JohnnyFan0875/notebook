# Databases

這個章節整理資料分析常見的關聯式資料庫筆記。對資料科學工作來說，SQL 不只是查資料，更是前置清理、聚合、抽樣與建立分析資料表的重要工具。

## Topics

- [MySQL](mysql.md)
- [PostgreSQL](postgresql.md)

## 建議使用時機

- 原始資料量太大，不適合先全部拉進 pandas。
- 需要在資料庫端先做 join、group by、window function 或條件過濾。
- 想把分析邏輯前移，減少本地端記憶體負擔與重複匯出流程。
