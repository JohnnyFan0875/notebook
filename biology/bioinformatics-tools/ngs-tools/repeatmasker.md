## Docker

- [pegi3s/repeat_masker](https://hub.docker.com/r/pegi3s/repeat_masker)

  - `-pa` for multi-processing

- ouput: `<filename>.out`
  - example: `463 1.3 0.6 1.7 chr1 10001 10468 (248945954) + (TAACCC)n Simple_repeat 1 463 (0) 1`

| #   | 欄位                | 意思                    |
| --- | ------------------- | ----------------------- |
| 1   | SW score            | 比對分數                |
| 2   | % div.              | 與 consensus 的差異率   |
| 3   | % del.              | deletion 比例           |
| 4   | % ins.              | insertion 比例          |
| 5   | query seq           | 染色體 / contig         |
| 6   | q.start             | repeat 在 genome 的起點 |
| 7   | q.end               | repeat 在 genome 的終點 |
| 8   | q.left              | 到染色體尾端剩餘長度    |
| 9   | strand              | `+` 或 `C`              |
| 10  | repeat name         | repeat 名稱             |
| 11  | repeat class/family | repeat 分類             |
| 12  | r.start             | repeat consensus 起點   |
| 13  | r.end               | repeat consensus 終點   |
| 14  | r.left              | consensus 剩餘長度      |
| 15  | ID                  | repeat ID（同源拷貝）   |
