# Explicit vs. Implicit Feedback

## Explicit Feedback

explicit feedback 是使用者直接表達偏好的訊號，例如：

- 星等評分
- like / dislike
- 問卷偏好分數

這類資料的好處是語意清楚。`5` 分通常可以被理解成比 `3` 分更喜歡。

MovieLens 就是典型的 explicit-rating 練習資料，適合拿來做 rating prediction 與 ALS 入門。

## Implicit Feedback

implicit feedback 不是直接評分，而是從行為推測偏好，例如：

- click
- view
- dwell time
- purchase
- stream count

這類資料在產品中更常見，但它的難點是：互動不一定等於喜歡，沒有互動也不一定等於不喜歡。

Million Song Dataset 這類音樂互動資料，常被當成 implicit recommendation 的範例。

## Why the Distinction Matters

explicit 與 implicit 的差異，不只是欄位名稱不同，而是整個建模假設都不同：

- explicit rating 比較像在學一個偏好分數
- implicit signal 比較像在學互動強弱與信心程度

因此在 PySpark ALS 中，`implicitPrefs` 不是小細節，而是切換建模模式的重要開關。

## The Role of Alpha

在 implicit recommendation 裡，`alpha` 常被用來調整 confidence weighting。

直覺上可以把它理解成：

- 互動次數越多，模型對「這可能代表偏好」的信心越高
- 但這個信心放大多少，需要透過 `alpha` 這類設定控制

所以 implicit recommendation 不只是在 rating 欄位裡塞一個 `0/1`，而是要重新思考觀測訊號與信心權重的關係。

## Practical Reminders

- explicit feedback 較少、較乾淨，但在真實產品裡往往更難大量取得。
- implicit feedback 量大、更新快，但噪音也更高。
- 如果你搞不清楚資料代表偏好還是只是曝光痕跡，先不要急著訓練模型。

[Back to Recommender Systems](README.md)
