# Java Performance and Concurrency

Performance work in Java usually starts with one rule:

Optimize the actual bottleneck, not the code that merely looks suspicious.

This note collects the early concepts that help reason about runtime cost, memory behavior, and basic parallel execution.

## Time Complexity

Time complexity describes how runtime grows as input size grows.

It does not try to predict exact milliseconds. It answers a structural question instead:

- what happens when the input gets much larger?

## Big-O

Big-O notation is the usual shorthand for worst-case growth.

Common classes:

| Complexity | Intuition |
| ---------- | --------- |
| `O(1)` | constant work |
| `O(n)` | work grows linearly with input size |
| `O(n^2)` | nested-loop style growth |

Example intuition:

- `ArrayList.get(index)` is typically `O(1)`
- linear search through a list is `O(n)`
- comparing every item to every other item often becomes `O(n^2)`

## Why Complexity Matters

The difference between `O(n)` and `O(n^2)` is easy to ignore on tiny inputs and painful on large ones.

That is why data-structure choice matters so much in Java code that processes collections at scale.

## Space Complexity

Space complexity describes how extra memory usage grows with input size.

Common intuition:

- `O(1)` extra space means the algorithm uses only a fixed amount of additional memory
- `O(n)` extra space means memory grows with the input
- `O(n^2)` extra space can become dangerous very quickly

Performance is not only about CPU time. Memory pressure can also become the real bottleneck.

## Picking Data Structures for Performance

The course material repeatedly points to one practical lesson:

- choose structures whose common operations match your workload

Examples:

- membership checks in a `List` are usually `O(n)`
- membership checks in a `HashSet` are usually `O(1)` on average
- key lookups in a `HashMap` are usually `O(1)` on average

So if the real job is repeated lookup by key or membership, a list may be the wrong default.

## Why Hash-Based Structures Feel Fast

Hash-based collections rely on `hashCode()` to map values into buckets.

That is why `HashSet` and `HashMap` are often described as `O(1)` on average rather than always `O(1)` in every possible case.

Key point: average-case speed depends on good hashing and healthy distribution.

## Performance Bottlenecks

A bottleneck is the part of a program that limits overall throughput or responsiveness.

Common categories:

- CPU-bound work
- I/O-bound work
- memory-bound work

Examples:

- expensive calculations are often CPU-bound
- database, network, or file waits are often I/O-bound
- object-heavy pipelines can become memory-bound

## Measure Before You Guess

Premature optimization is often wasted effort.

A better sequence is:

1. identify the slow path
2. measure it
3. change the design
4. measure again

## Timing with `System.nanoTime()`

For small runtime measurements, `System.nanoTime()` is the usual Java tool.

```java
long start = System.nanoTime();

// code under measurement

long end = System.nanoTime();
long duration = end - start;
```

It measures elapsed time and is more appropriate for benchmarking than wall-clock APIs like `System.currentTimeMillis()`.

## Benchmarking Caution

One timing result is not a performance truth.

Small Java benchmarks can be distorted by:

- JVM warm-up
- garbage collection
- cache effects
- different input shapes

For notebook-level reasoning, `nanoTime()` is enough to build intuition. For serious measurement, use proper benchmarking tools.

## JVM Memory Basics

At a high level, Java memory discussions usually separate:

| Area | Typical role |
| ---- | ------------ |
| stack | call frames, local primitive values, references |
| heap | objects and arrays |

This is a simplification, but it is a helpful one.

## Runtime Memory Metrics

`Runtime.getRuntime()` exposes a few practical memory metrics:

```java
Runtime runtime = Runtime.getRuntime();

long maxMemory = runtime.maxMemory();
long totalMemory = runtime.totalMemory();
long freeMemory = runtime.freeMemory();
```

Useful meanings:

- `maxMemory()` is the maximum heap the JVM will try to use
- `totalMemory()` is currently allocated memory
- `freeMemory()` is unused memory inside that current allocation

## Garbage Collection

Java automatically reclaims unreachable objects through garbage collection.

That means developers usually do not free memory manually, but it does not mean memory usage stops mattering.

Important intuition:

- too many unnecessary allocations can still hurt performance
- garbage collection pauses and churn are real costs
- object lifetime patterns influence runtime behavior

## Avoiding Needless Allocation

A classic example is string building in loops.

```java
StringBuilder builder = new StringBuilder();

for (String part : parts) {
    builder.append(part);
}

String result = builder.toString();
```

`StringBuilder` is usually better than repeated string concatenation in a loop because it avoids creating many intermediate string objects.

## Profile First

If optimization is on the table, profiling should come before aggressive rewrites.

The source material mentions tools such as:

- `JVisualVM`
- `jmap`

The main takeaway is not tool memorization. It is process:

- inspect real CPU and memory behavior
- optimize the hot path
- ignore the cold path unless evidence says otherwise

## Sequential vs Parallel Execution

Sequential execution does one step after another on a single flow.

Parallel execution tries to overlap work across multiple threads or cores.

That can improve throughput, but only when the task is suitable and the coordination cost does not erase the benefit.

## Threads

A thread is a unit of execution inside the program.

Basic thread creation can look like:

```java
Runnable task = () -> {
    System.out.println(Thread.currentThread().getName());
};

Thread thread = new Thread(task);
thread.start();
```

This launches a separate execution path.

## Thread Pools

Creating raw threads repeatedly is often not the best design.

Thread pools let the runtime reuse worker threads rather than creating a new one for every small task.

That is the main reason higher-level concurrency tools are usually preferred in real applications.

## Parallel Streams

Java streams can also run in parallel:

```java
List<Integer> result = numbers.parallelStream()
    .map(n -> n * 2)
    .toList();
```

This can simplify some data-parallel collection work.

But parallel streams are not automatically faster.

They tend to help more when:

- the workload per element is meaningful
- the input is large enough
- the operations are independent

They tend to help less when:

- work per element is tiny
- ordering constraints matter
- the overhead of splitting and coordination dominates

## Caching

Caching trades memory for speed by storing expensive results for reuse.

A simple in-memory cache often starts with a `HashMap`.

```java
private final Map<String, UserProfile> cache = new HashMap<>();
```

Common benefits:

- fewer repeated computations
- fewer repeated database or network calls
- lower latency on hot reads

## Cache Tradeoffs

Caches are useful, but they introduce design questions:

- how long should entries live?
- when should data expire?
- what happens when memory fills up?
- how stale can cached data become?

That is why production caches often need eviction and expiration policies rather than unbounded growth.

## Optimization Heuristics

Good default habits:

- fix the algorithm before micro-tuning syntax
- measure before and after changes
- reduce unnecessary allocation in hot loops
- use better data structures before adding concurrency
- add concurrency only when the problem is actually parallel-friendly
- use caching when the recomputation cost is meaningfully higher than the memory cost

## Common Traps

- treating Big-O as exact runtime prediction
- benchmarking once and trusting the number blindly
- optimizing cold code instead of the real bottleneck
- assuming parallel execution is always faster
- using a `List` for repeated membership checks that really want a `Set`
- growing caches without expiration or eviction strategy
- forgetting that lower allocation pressure can matter as much as raw CPU work

## Related Notes

- [Java Collections and Exception Handling](java-collections-and-exception-handling.md)
- [Java File I/O and Streams](java-file-io-and-streams.md)
- [Java Testing](java-testing.md)
