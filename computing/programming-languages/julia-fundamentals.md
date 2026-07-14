# Julia Fundamentals

Julia is a general-purpose language designed with scientific computing, statistics, and data work in mind.

The beginner mental model is:

- Python-like readability
- R- and MATLAB-friendly data-science ergonomics
- stronger focus on performance than many scripting languages

## Why Julia Exists

Julia was designed to be pleasant for high-level programming without giving up serious numerical computing use cases.

That is why Julia often shows up in workflows involving:

- data science
- linear algebra
- simulation
- scientific computing

## Basic Expressions

Julia can be used interactively as a calculator-like environment.

```julia
println(1 + 2)
println(2 * 3)
```

`println(...)` prints a value and moves to a new line.

## Variables

Julia variables are assigned with `=`.

```julia
x = 3
double_x = x * 2

println(x)
println(double_x)
```

Naming style is usually lowercase, often with underscores when they improve readability.

## Core Types

Some high-frequency Julia types are:

| Type | Example |
| ---- | ------- |
| `Int64` | `3` |
| `Float64` | `3.14` |
| `Bool` | `true` |
| `String` | `"Jane"` |
| `Char` | `'a'` |

You can inspect a value's type with `typeof(...)`.

```julia
println(typeof(3))
println(typeof(3.14))
println(typeof(true))
println(typeof("Jane"))
```

## Converting Values

Julia does not automatically pretend that strings and numbers are interchangeable.

Common conversions:

```julia
x = "1"

as_int = parse(Int64, x)
as_float = parse(Float64, x)
as_string = string(1)
```

Use `parse(...)` when text should become a number, and `string(...)` when a value should become text.

## Strings

Strings use double quotes.

```julia
name = "Jane"
book = "It is a truth universally acknowledged..."
```

Triple quotes are useful for multi-line text:

```julia
poem = """Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!"""
```

## String Concatenation and Interpolation

Julia commonly joins strings with `*`.

```julia
greeting = "Hello "
name = "Jane"

println(greeting * name)
```

Interpolation is often more readable:

```julia
row = 4
number = 12

println("Your seat is in row $row, seat number $number.")
println("The product is $(row * number)")
```

## Arrays

Julia arrays are central to both general programming and numerical work.

```julia
names = ["Ana", "Ben", "Cara"]
numbers = [1, 2, 3]
```

Useful inspection helpers:

```julia
println(typeof(names))
println(eltype(names))
```

- `typeof(x)` tells you the container type
- `eltype(x)` tells you the element type

## Indexing

Julia arrays are `1`-indexed, not `0`-indexed.

```julia
println(names[1])
println(names[end])
println(names[1:2])
```

That one-based indexing is one of the first habits to internalize when coming from Python, JavaScript, or Java.

## Building and Updating Arrays

```julia
x = String[]
push!(x, "first")
push!(x, "second")
```

The `!` convention in Julia usually signals that a function mutates its argument.

## Broadcasting

Broadcasting applies an operation elementwise with dot syntax.

```julia
a = [1, 2, 3]
b = [10, 20, 30]

println(a .+ 2)
println(a .+ b)
println(a .* 5)
println(a ./ 2)
```

This is a very Julia-specific habit worth learning early.

Without the dot, the operation can mean something different or fail entirely depending on the values involved.

## Conditionals

Julia conditionals use `if`, `elseif`, `else`, and `end`.

```julia
is_raining = true

if is_raining
    println("Better get your coat")
end
```

Multiple branches look like:

```julia
if score >= 90
    println("Excellent")
elseif score >= 70
    println("Good effort")
else
    println("Keep trying")
end
```

## Comparisons

Common comparison operators:

| Operator | Meaning |
| -------- | ------- |
| `==` | equal |
| `!=` | not equal |
| `>` | greater than |
| `>=` | greater than or equal |
| `<` | less than |
| `<=` | less than or equal |

These are frequently used inside `if` conditions and filters.

## Loops

The source material introduces both `for` and `while`.

```julia
for name in names
    println(name)
end
```

```julia
counter = 1

while counter <= 3
    println(counter)
    counter += 1
end
```

Julia closes both loop forms with `end`.

## Functions

Functions are defined with the `function` keyword.

```julia
function double(x)
    return x * 2
end
```

Then called normally:

```julia
println(double(2))
println(double(10.0))
```

## Multiple Dispatch

Multiple dispatch is one of Julia's signature ideas.

You can define different method implementations for different argument types:

```julia
function double(x::String)
    return x * x
end

function double(x::Bool)
    return !x
end
```

This means function behavior can vary by type in a first-class way, rather than being treated as a special advanced feature.

## DataFrames and CSV

For tabular work, the common packages are:

- `DataFrames.jl`
- `CSV.jl`

Basic setup:

```julia
using DataFrames
using CSV
```

## Creating a DataFrame

```julia
df = DataFrame(
    day = ["Wednesday", "Monday", "Thursday"],
    distance = [2000, 5000, 3500],
    time = [14.99, 31.68, 22.02],
    raining = [true, false, true]
)
```

This is the Julia equivalent of starting a small in-memory table for analysis.

## Loading CSV into a DataFrame

```julia
file = CSV.File("run.csv")
df = DataFrame(file)
```

Key point: use `CSV.File(...)`, not a generic `File(...)` constructor.

## Inspecting a DataFrame

Useful early operations:

```julia
println(first(df, 3))
println(names(df))
println(size(df))
println(describe(df))
```

These help answer:

- what columns exist?
- how big is the table?
- what do the first few rows look like?
- what are the rough summaries?

## Selecting Data

Examples of common selection patterns:

```julia
value = df[2, 3]
column = df[:, 2]
subset = df[:, 1:3]
row = df[4, :]
rows = df[2:4, :]
```

This is a core piece of Julia tabular work: rows and columns are selected through indexing syntax rather than only through method chains.

## Sorting and Filtering DataFrames

Sorting:

```julia
df_sorted = sort(df, :distance)
```

Filtering:

```julia
df_monday = filter(row -> row.day == "Monday", df)
df_short = filter(row -> row.distance <= 3000, df)
df_raining = filter(row -> row.raining, df)
```

This is a concise way to keep only rows that match a condition.

## Derived Columns

Julia also makes it easy to compute new arrays from existing columns.

```julia
distance_km = df.distance ./ 1000
time_hr = df.time ./ 60
speeds = distance_km ./ time_hr
```

This is where broadcasting and column-oriented data analysis naturally meet.

## Common Traps

- forgetting that Julia arrays are `1`-indexed
- confusing `String` and `Char`
- forgetting to use `parse(...)` when converting text to numbers
- forgetting dot syntax for elementwise array operations
- assuming functions should behave the same for all types when multiple dispatch is available
- mixing up raw CSV loading with `DataFrame` construction

## Related Notes

- [Java Fundamentals](java-fundamentals.md)
- [Java Control Flow and Methods](java-control-flow-and-methods.md)
