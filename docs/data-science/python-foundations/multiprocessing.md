# Python Multiprocessing

## Overview

- The **multiprocessing** module in Python allows you to create and manage separate processes, enabling true parallelism.
- Useful for CPU-bound tasks (e.g., numerical computations, data processing) because it bypasses the Global Interpreter Lock (GIL).
- Provides higher-level abstractions like `Pool` for parallel execution and low-level APIs like `Process` for manual control.

## Key Concepts

- **Process**: Independent execution unit with its own memory space.
- **Pool**: A convenient way to parallelize a function across multiple inputs.
- **Process class**: Allows you to manually spawn and control processes.
- **Communication**: Can be achieved using `Queue`, `Pipe`, or shared memory objects.

## Example 1: Parallel Square Computation with Pool

```python
import multiprocessing as mp

# Function to compute square of a number
def square(x):
    return x * x

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]

    # Create a Pool with 4 worker processes
    with mp.Pool(processes=4) as pool:
        results = pool.map(square, numbers)

    print("Input numbers:", numbers)
    print("Squared results:", results)
```

**Output:**

```
Input numbers: [1, 2, 3, 4, 5]
Squared results: [1, 4, 9, 16, 25]
```

## Example 2: Launching Processes Manually with Process

```python
from multiprocessing import Process

def function1(v1):
    print("Function1:", v1)

def function2(v2):
    print("Function2:", v2)

if __name__ == "__main__":
    v1, v2 = "Hello", "World"

    p1 = Process(target=function1, args=(v1,))
    p2 = Process(target=function2, args=(v2,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
```

**Output (order may vary):**

```
Function1: Hello
Function2: World
```

## When to Use Pool vs Process

- **Pool**: Best when you need to apply the _same function_ across many items (e.g., compute squares of a list of numbers, process many files). The workload is homogeneous and can be evenly distributed among worker processes.
- **Process**: Best when you need to run _different functions or tasks_ in parallel (e.g., one process downloads data, another cleans it, another analyzes it). It gives you finer control but requires more manual management.

## Notes & Best Practices

- Always guard code with `if __name__ == "__main__":` when using multiprocessing in Python (especially on Windows and macOS).
- For I/O-bound tasks, consider using `concurrent.futures.ThreadPoolExecutor` or `asyncio` instead.
- Be mindful of overhead: starting processes has a cost, so multiprocessing shines with **large workloads**.
- Use `Pool` for **batching the same function across many inputs**.
- Use `Process` for **custom workflows** where each process runs a different function.

> Use `multiprocessing` when you need to fully utilize multiple CPU cores for heavy computations.
