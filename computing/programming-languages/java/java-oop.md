[程式語言](../README.md) › [Java](README.md) › OOP

# Java 物件導向 (Java OOP)

從一個實際問題出發：怎麼把「有資料也有行為的東西」建模，讓程式長大後仍然有條理？這引出類別、物件、封裝、繼承、介面與多型。範式層次的比較見 [程式設計範式](../../computer-science-foundations/programming-paradigms.md#物件導向-object-oriented)。

## 類別與物件

```java
public class Car {
    private String model;                     // 欄位 (field)：資料；private 隱藏內部
    private int year;
    public static int wheels = 4;             // static：屬於類別，所有物件共用

    public Car(String model, int year) {      // 建構子：與類別同名、沒有回傳型別
        this.model = model;                   // this.model 是欄位，model 是參數
        this.year = year;
    }

    public Car(String model) {                // 多載的建構子
        this(model, 2024);                    // 呼叫另一個建構子
    }

    public String getModel() { return model; }            // getter
    public void setYear(int year) {                       // setter：可在此加驗證
        if (year < 1886) throw new IllegalArgumentException("year too early");
        this.year = year;
    }

    public void drive() { System.out.println(model + " driving"); }   // 方法：行為
}

Car c = new Car("Corolla", 2020);             // 物件 = 類別的實例
c.drive();
```

| 概念 | 意義 |
| --- | --- |
| 類別 (class) | 藍圖（餅乾模具） |
| 物件 (object / instance) | 依藍圖建出的個體（餅乾），有自己的狀態 |
| 建構子 (constructor) | 建立物件時執行，確保初始狀態有效 |
| `this` | 目前這個物件 |
| `static` 成員 | 屬於類別而非個別物件：`Car.wheels`、`Math.max()` |

## 封裝與存取修飾詞

封裝 (encapsulation)：把內部細節藏在受控的公開介面之後。外部透過方法操作，內部表示可以改變而不影響呼叫端。

| 修飾詞 | 誰能存取 |
| --- | --- |
| `public` | 所有人 |
| `protected` | 同 package + 子類別 |
| （不寫，package-private） | 同 package |
| `private` | 只有類別自己 |

> 欄位預設 `private`，透過 getter / setter 存取；即使 setter 目前只是轉存值，方法邊界也保留了日後加驗證的空間。

### 資料類別：POJO 與 record

POJO (Plain Old Java Object) 是主要用來存放與傳遞資料的類別：`private` 欄位、公開 getter / setter（布林用 `isActive()`）、無參數建構子，不依賴特定框架、不放商業邏輯。

Java 16+ 的 `record` 用一行定義**不可變**的資料類別，自動產生建構子、存取方法、`equals`、`hashCode`、`toString`：

```java
public record Sample(String id, String tissue, double readsM) {
    public Sample {                                     // 精簡建構子：驗證
        if (readsM <= 0) throw new IllegalArgumentException("readsM must be > 0");
    }
}

Sample s = new Sample("S1", "liver", 32.1);
s.id();                                                 // "S1"（存取方法沒有 get 前綴）
s.equals(new Sample("S1", "liver", 32.1));              // true：依內容比較
```

| 需要 | 選擇 |
| --- | --- |
| 不可變的資料載體（DTO、查詢結果、設定） | `record` |
| 需要 setter、框架要求無參數建構子（JPA、舊版序列化） | POJO |

> 自訂類別要放進 `HashSet` / 當 `HashMap` 的 key 時，必須同時覆寫 `equals` 與 `hashCode`（record 已自動產生）。

## 繼承

```java
public class Vehicle {
    protected String model;
    public Vehicle(String model) { this.model = model; }
    public void drive() { System.out.println("Driving"); }
}

public class Truck extends Vehicle {                  // Truck is-a Vehicle
    public Truck(String model) { super(model); }      // super：呼叫父類別建構子
    @Override                                         // 讓編譯器檢查真的有覆寫到
    public void drive() { System.out.println(model + " hauling"); }
}
```

| 名詞 | 意義 |
| --- | --- |
| 父類別 (superclass / base class) | 被繼承的類別 |
| 子類別 (subclass) | 用 `extends` 繼承；Java 只能單一繼承 |
| 覆寫 (overriding) | 子類別重新實作繼承來的方法（同簽章） |
| 多載 (overloading) | 同名方法、不同參數列（`drive()`、`drive(int speed)`），編譯時依參數選擇 |
| `final` 類別 / 方法 | 不能被繼承 / 覆寫 |

> 繼承只用在真正的 is-a 關係且父類別抽象穩定時；父類別太廣會讓子類別繼承到不適合的成員。需要組裝行為時用組合（欄位持有其他物件）。

## 抽象類別與介面

```java
abstract class Shape {                               // 不能直接 new
    abstract double area();                          // 抽象方法：子類別必須實作
    void describe() { System.out.println("Area = " + area()); }   // 可有共用實作
}

interface Chargeable {                               // 能力契約 (can-do)
    void charge();
    default String plug() { return "Type 2"; }       // Java 8+：介面可有預設方法
}

class ElectricCar extends Vehicle implements Chargeable {   // 單一繼承 + 多個介面
    ElectricCar(String model) { super(model); }
    @Override public void charge() { System.out.println("Charging"); }
}
```

| | 抽象類別 | 介面 |
| --- | --- | --- |
| 表達 | is-a，有共同狀態與部分實作 | can-do，能力契約 |
| 欄位 | 可有實例欄位 | 只有常數 |
| 一個類別可以 | 繼承一個 | 實作多個 |
| 何時用 | 一群相關類別共享程式碼 | 不相關的類別要提供同一種能力（`Comparable`、`Runnable`） |

## 多型 (Polymorphism)

以一般型別的變數持有不同的具體物件，執行時呼叫實際物件的實作：

```java
List<Vehicle> fleet = List.of(new Vehicle("Van"), new Truck("Hino"), new ElectricCar("Model 3"));
for (Vehicle v : fleet) {
    v.drive();                       // 各自呼叫自己的 drive()
}

List<String> names = new ArrayList<>();   // 宣告用介面型別，實作可以替換
```

多型讓程式少寫一堆 `if (type == ...)`：新增一種類別只要實作同一個介面，呼叫端不用改。

## 常見混淆

| 容易混淆 | 差別 |
| --- | --- |
| 類別 vs 物件 | 藍圖 vs 實例 |
| 覆寫 vs 多載 | 繼承時改行為（執行時決定）vs 同名不同參數（編譯時決定） |
| 抽象類別 vs 介面 | is-a + 共享實作 vs can-do 契約 |
| 實例成員 vs `static` 成員 | 每個物件各一份 vs 整個類別共用一份 |
| `==` vs `equals` | 是否同一物件 vs 內容是否相等 |

| 常見錯誤 | 說明 |
| --- | --- |
| 把繼承當預設的重用方式 | 優先組合與介面 |
| 太早把欄位設為 `public` | 失去封裝 |
| 建構子寫了回傳型別（`void Car()`） | 變成普通方法，不是建構子 |
| 覆寫 `equals` 卻沒覆寫 `hashCode` | `HashSet` / `HashMap` 行為錯誤 |
