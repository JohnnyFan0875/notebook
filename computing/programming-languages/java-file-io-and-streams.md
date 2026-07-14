# Java File I/O and Streams

This note focuses on two adjacent but different ideas that often get taught together in Java:

- file and directory operations through `java.io`
- collection-processing streams through the Stream API

They both move data around, but they solve different problems. File I/O is about persistence and the filesystem. Stream processing is about transforming in-memory data collections.

## File Basics with `File`

The older `java.io.File` API represents a path-like handle to a file or directory.

```java
import java.io.File;

File dataTextFile = new File("data.txt");
```

By itself, creating a `File` object does not create anything on disk. It just points to a location.

## Creating Files

```java
import java.io.File;
import java.io.IOException;

File dataTextFile = new File("data.txt");
boolean created = dataTextFile.createNewFile();
```

`createNewFile()` returns:

- `true` if the file was actually created
- `false` if it already existed

Because creation can fail, this usually belongs inside `try/catch`.

## Deleting Files

```java
File exampleFile = new File("example.txt");
boolean deleted = exampleFile.delete();
```

The return value tells you whether deletion succeeded.

Key point: file APIs frequently communicate success through both return values and exceptions. You should inspect both design patterns instead of assuming one universal style.

## Checking Existence

```java
if (dataTextFile.exists()) {
    System.out.println("The file already exists.");
}
```

This is useful for guard checks before create, overwrite, or delete operations.

## Wrap File Operations in `try/catch`

```java
try {
    File dataTextFile = new File("data.txt");
    dataTextFile.createNewFile();
} catch (IOException e) {
    System.out.println(e.getMessage());
}
```

Typical reasons for failure include:

- invalid paths
- missing permissions
- other filesystem-level issues

## Reading Files with `FileReader`

`FileReader` is a character-oriented reader for text files.

```java
import java.io.FileReader;
import java.io.IOException;

FileReader fr = new FileReader("example.txt");
int data = fr.read();
while (data != -1) {
    System.out.print((char) data);
    data = fr.read();
}
fr.close();
```

A few important details:

- `read()` returns an `int`
- `-1` means end-of-file
- character output often requires casting from `int` to `char`

## Reading Efficiently with `BufferedReader`

For larger text workloads, buffered reading is usually better.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

BufferedReader br = new BufferedReader(new FileReader("example.txt"));
String line;

while ((line = br.readLine()) != null) {
    System.out.println(line);
}

br.close();
```

Why use it:

- reads line by line
- reduces low-level read calls
- more practical than character-by-character reading for ordinary text files

## Writing Files with `FileWriter`

```java
import java.io.FileWriter;
import java.io.IOException;

FileWriter fw = new FileWriter("example.txt");
fw.write("Hello, Java");
fw.close();
```

Warning: plain `FileWriter("example.txt")` overwrites existing content by default.

## Appending Instead of Overwriting

```java
FileWriter fw = new FileWriter("example.txt", true);
fw.write("More text");
fw.close();
```

The second `true` argument enables append mode.

## Writing Efficiently with `BufferedWriter`

```java
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

BufferedWriter bw = new BufferedWriter(new FileWriter("example.txt"));
bw.write("Hello");
bw.newLine();
bw.write("World");
bw.close();
```

This is usually the better choice when writing more than tiny one-off text snippets.

## Directories

`File` can also represent directories.

```java
File newDirectory = new File("myDirectory");
boolean created = newDirectory.mkdir();
```

Key point: whether a `File` object ends up representing a file or a directory depends on what operation you perform with it.

## Listing Files in a Directory

```java
File dir = new File("myDirectory");
File[] files = dir.listFiles();
```

`listFiles()` returns:

- an array of `File` objects when the directory exists
- `null` when it does not

So it should be checked before use.

## Relative vs Absolute Paths

```java
File file = new File("myDirectory/sample.txt");

String relative = file.getPath();
String absolute = file.getAbsolutePath();
```

- relative path: interpreted from the current working directory
- absolute path: full filesystem location

Understanding this difference prevents many "it works on my machine" path bugs.

## For-Each vs Iterator

Moving to in-memory collections:

```java
for (String x : fruits) {
    System.out.println(x);
}
```

The for-each loop is the simplest traversal style when you only need to read elements.

## `Iterator`

Use `Iterator` when you need explicit traversal control or safe removal during iteration.

```java
import java.util.Iterator;

Iterator<String> it = fruits.iterator();
while (it.hasNext()) {
    String fruit = it.next();
    if (fruit.startsWith("A")) {
        it.remove();
    }
}
```

Key point: removing through the iterator is the safe pattern here; it avoids `ConcurrentModificationException`.

## `ListIterator`

`ListIterator` extends the iterator idea for lists.

```java
import java.util.ListIterator;

ListIterator<String> it = names.listIterator();
while (it.hasNext()) {
    String name = it.next();
    if ("Bob".equals(name)) {
        it.set("Bobby");
    }
}
```

Useful capabilities:

- move forward with `.next()`
- move backward with `.previous()`
- modify current element with `.set()`
- insert during iteration with `.add()`

## Stream API

Java streams process collections in a more functional style.

```java
names.stream().forEach(name -> System.out.println(name));
```

A stream is not the same thing as a file stream here. In this context, it is a pipeline abstraction over in-memory data.

## Creating a Stream

```java
Stream<String> stream = names.stream();
```

This is the entry point from a collection into stream-style processing.

## Filtering

```java
names.stream()
    .filter(name -> name.startsWith("A"))
    .forEach(System.out::println);
```

Use `.filter()` when you want to keep only matching elements.

## Counting

```java
long count = names.stream()
    .filter(name -> name.startsWith("B"))
    .count();
```

`.count()` returns `long`.

## Transforming with `map()`

```java
Set<String> upper = names.stream()
    .map(name -> name.toUpperCase())
    .collect(Collectors.toSet());
```

`map()` transforms each element into another form.

## Aggregating with `reduce()`

```java
int totalLength = names.stream()
    .map(name -> name.length())
    .reduce(0, (sum, length) -> sum + length);
```

Use `reduce()` when the goal is one accumulated result.

## When Streams Help

Streams are especially useful when you want:

- readable filter / map / aggregate pipelines
- transformation into a new result collection
- less manual loop boilerplate

They are less attractive when:

- you are mutating the original collection heavily
- the loop is very small and direct imperative code is clearer

## Interview Fast Answer

If someone asks for the practical difference between `Iterator` and streams, a good short answer is:

- `Iterator` is about explicit step-by-step traversal and safe in-loop mutation
- streams are about declarative transformation pipelines over collections

If the follow-up is about file I/O, the highest-signal distinction is:

- `File` models file/directory locations
- `FileReader` / `BufferedReader` read text
- `FileWriter` / `BufferedWriter` write text
- buffering improves efficiency for larger workloads

## Common Traps

- assuming `new File(...)` creates the file immediately
- forgetting that `FileWriter` overwrites by default
- forgetting to close readers and writers
- removing collection elements inside for-each instead of through `Iterator`
- confusing Java Stream API with low-level I/O streams
- overusing streams where a small loop would be easier to read

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
