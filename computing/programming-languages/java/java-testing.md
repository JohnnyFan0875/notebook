[程式語言](../README.md) › [Java](README.md) › 測試

# Java 測試 (Java Testing)

用 JUnit 寫單元測試、用 Mockito 隔離依賴、用參數化測試涵蓋多組輸入。測試的目的：確認正常行為，並刻意探測邊界與失敗路徑；只在 happy path 能跑的程式等於沒測。測試層級與 Python 的 pytest 寫法見 [測試](../../../data-science/python-foundations/testing.md)。

## 邊界情況 (Edge Cases)

| 類型 | 例子 |
| --- | --- |
| 空值 | `null`、空字串、空集合 |
| 數值邊界 | 0、負數、`Integer.MAX_VALUE`、溢位 |
| 規則邊界 | 剛好在驗證門檻上、差一點點的值 |
| 格式 | 多餘空白、大小寫、非預期字元 |

## JUnit 基本寫法

JUnit Jupiter（JUnit 5 起的 API）是 Java 的標準測試框架；Maven / Gradle 專案的測試放在 `src/test/java/`，以 `mvn test` 或 `gradle test` 執行。

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    @Test
    void add_twoPositives_returnsSum() {
        // Arrange：準備輸入
        Calculator calc = new Calculator();
        // Act：呼叫受測程式
        int actual = calc.add(2, 2);
        // Assert：檢查結果
        assertEquals(4, actual);                       // 預期值在前、實際值在後
    }

    @Test
    void parse_badInput_throws() {
        assertThrows(NumberFormatException.class, () -> Integer.parseInt("abc"));
    }
}
```

| 斷言 | 用途 |
| --- | --- |
| `assertEquals(expected, actual)` | 相等；浮點數加容許誤差 `assertEquals(0.3, x, 1e-9)` |
| `assertTrue` / `assertFalse` | 條件 |
| `assertNull` / `assertNotNull` | 空值 |
| `assertThrows(Type.class, () -> ...)` | 預期丟出例外（失敗行為也是契約的一部分） |
| `assertAll(...)` | 多個斷言一起回報 |

| 註解 | 用途 |
| --- | --- |
| `@Test` | 標記測試方法 |
| `@BeforeEach` / `@AfterEach` | 每個測試前後的準備與清理 |
| `@BeforeAll` / `@AfterAll` | 整個類別前後執行一次（`static`） |
| `@Disabled` | 暫時跳過 |
| `@DisplayName` | 報告中顯示的名稱 |

測試命名用 `方法_情境_預期結果`：`isValidUsername_null_returnsFalse`。CI 輸出失敗時，不必打開程式碼就知道哪個行為壞了。

## 單元測試 vs 整合測試

| | 單元測試 | 整合測試 |
| --- | --- | --- |
| 範圍 | 單一元件，隔離依賴 | 多個元件一起運作 |
| 速度 | 快 | 慢 |
| 失敗時 | 容易定位 | 要追查較多 |
| 依賴 | 用 mock 取代 | 真實（測試資料庫、容器） |
| 優化 | 精確與速度 | 真實性 |

## Mockito：隔離依賴

依賴 (dependency) 是程式所依靠的其他元件：API client、資料庫層、外部服務。依賴慢、不確定或不受控時，單元測試用 mock 取代它。

```java
import static org.mockito.Mockito.*;

@Test
void convert_mockedRate_returnsExpectedAmount() {
    RateServer bank = mock(RateServer.class);                 // 建立假的依賴
    when(bank.getRateEuroTo("JPY")).thenReturn(110.0);        // stubbing：設定回傳值

    Converter conv = new Converter(bank);                     // 依賴從建構子注入，才能替換
    assertEquals(1100.0, conv.convert(10, "JPY"), 1e-9);

    verify(bank).getRateEuroTo("JPY");                        // 驗證互動：確實呼叫了一次
    verifyNoMoreInteractions(bank);
}
```

| 重點 | 說明 |
| --- | --- |
| 沒 stub 的方法 | 回傳預設值（`0`、`false`、`null`、空集合），常讓測試以令人困惑的方式失敗 |
| `verify` 何時用 | 「有沒有呼叫」本身就是需求時（例如錯誤時要寫入 error store、成功時不寫） |
| 可測試的設計 | 依賴透過建構子傳入，而不是在類別內 `new` |

## 參數化測試

同一段邏輯用多組輸入驗證，避免複製貼上一堆幾乎相同的 `@Test`。

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import java.util.stream.Stream;

@ParameterizedTest
@NullSource                                                // 加入 null（@ValueSource 不能放 null）
@ValueSource(strings = {"", "jane doe", "a"})              // 每組一個值；屬性名是複數 strings / ints
void isValidUsername_invalid_returnsFalse(String username) {
    assertFalse(Validator.isValidUsername(username));
}

@ParameterizedTest
@CsvSource({
    "Hello World, 11",
    "DataCamp,    8",
    "'',          0"                                       // '' 代表空字串
})
void length_returnsExpected(String text, int expected) {
    assertEquals(expected, text.length());
}

@ParameterizedTest
@MethodSource("people")                                    // 物件等複雜輸入
void fullName_returnsExpected(Person p, String expected) {
    assertEquals(expected, p.fullName());
}
static Stream<Arguments> people() {
    return Stream.of(
        Arguments.of(new Person("John", "Doe"), "John Doe"),
        Arguments.of(new Person("Jane", "Doe"), "Jane Doe"));
}
```

| 來源 | 何時用 |
| --- | --- |
| `@ValueSource` | 單一簡單值 |
| `@NullSource` / `@EmptySource` / `@NullAndEmptySource` | 加入 `null` / 空值 |
| `@CsvSource` | 小型的多欄輸入 / 預期輸出表 |
| `@MethodSource` | 物件或需要程式產生的輸入 |
| `@EnumSource` | 每個 enum 值各測一次 |

## 常見錯誤

| 錯誤 | 說明 |
| --- | --- |
| 只測 happy path | 邊界與錯誤路徑最容易出 bug |
| `assertEquals` 參數順序顛倒 | 失敗訊息的「預期 / 實際」會反過來 |
| 能用快速單元測試卻寫成整合測試 | 測試變慢、難定位 |
| mock 沒有 stub | 回傳預設值造成誤導 |
| 差異很大的案例硬塞進同一個參數化測試 | 可讀性變差 |
| 測試之間共享可變狀態 | 執行順序不同結果就不同 |
