# Julia Intermediate Patterns

This note picks up where basic Julia syntax leaves off.

The focus here is on language patterns that become useful once you already know variables, arrays, conditionals, and simple functions:

- richer iteration
- immutable and keyed data structures
- more flexible function signatures
- lightweight performance measurement
- practical DataFrame cleanup

## Iteration with `for`

Julia `for` loops iterate directly over values rather than forcing index-based access.

```julia
shopping_list = ["Apples", "Bread", "Carrots", "Strawberries"]

for item in shopping_list
    println(item)
end
```

This is usually clearer than manually indexing each element.

## `enumerate`

When you need both the index and the value, use `enumerate(...)`.

```julia
for (index, item) in enumerate(shopping_list)
    println("$index => $item")
end
```

This is the common Julia pattern for "loop with position".

## `while`

`while` is still useful when repetition depends on a changing condition rather than a simple iterable.

```julia
counter = 10

while counter != 0
    println(counter)
    counter -= 1
end
```

As usual, the critical question is what makes the condition become false.

## Ranges

Ranges are first-class Julia values and show up constantly in iteration.

```julia
my_range = 1:2:9
```

This means:

- start at `1`
- step by `2`
- stop at `9`

You can loop over the range directly:

```julia
for value in my_range
    println(value)
end
```

Useful accessors include `start`, `step`, and `stop`.

## The Splat Operator

The splat operator `...` expands a collection into separate arguments.

```julia
values = [1, 2, 3]
println(values...)
```

This becomes especially useful when forwarding variable-length argument lists.

## Tuples

A tuple is an ordered immutable collection.

```julia
my_tuple = (10, 20, 30, 40)
my_mixed_tuple = (10, "Hello", 30, true)
```

Tuples can hold mixed types, and they support indexing like vectors.

```julia
println(my_tuple[1])
println(my_tuple[2:3])
```

## Why Use Tuples

Tuples are helpful when:

- the number of elements should not change
- the values represent one fixed grouped record
- you want lower-overhead immutable structure

Tradeoff:

- you cannot append, delete, or mutate elements after creation

## Immutability

Tuple immutability is a real design constraint, not just a style preference.

The following ideas do not work on tuples:

- `append!`
- element reassignment

That makes tuples safer for fixed-shape data, but worse for evolving collections.

## Named Tuples

A `NamedTuple` adds names to tuple fields.

```julia
person = (name = "Anthony", country = "Australia", city = "Sydney")

println(person[1])
println(person.name)
```

This is often a nice middle ground between raw tuples and full custom structs.

## Dictionaries

Julia dictionaries store key-value associations.

```julia
stock = Dict("ticker" => "AAPL", "price" => 131.86)
```

Use a dictionary when lookup by key is the real job.

## Typed vs Untyped Dictionaries

Untyped or loosely typed dictionaries are flexible but can become messy.

Julia also lets you declare dictionary types explicitly.

```julia
stock = Dict{String, Any}("ticker" => "AAPL", "price" => 131.86)
```

Key point: tighter types improve clarity and can improve performance, but only when they match the real data shape.

## Iterating Through Dictionaries

You can iterate over dictionary pairs directly:

```julia
for item in stock
    println(item)
end
```

Or iterate more explicitly:

```julia
for key in keys(stock)
    println(key)
end

for value in values(stock)
    println(value)
end
```

Tuple unpacking is often the cleanest form:

```julia
for (ticker, price) in stock
    println("$ticker => $price")
end
```

## Safe Lookup with `get`

Use `get(...)` when a key may not exist and you want a default.

```julia
price = get(stock, "price", 0.0)
```

This avoids immediate failure for missing keys.

## Dictionary Mutation

Dictionaries are mutable, so you can add or update entries.

```julia
stock["volume"] = 62128300
stock["price"] = 125.27
```

That is one of the main differences from tuples.

## Measuring Execution Time

Julia makes lightweight performance measurement accessible very early.

The simplest built-in option is the `@time` macro.

```julia
@time my_function()
```

It reports runtime and allocation information.

## `@time` Caveat

The first call often includes compilation overhead, so the first number can be misleading.

That means a quick mental rule is:

- first timing often reflects compilation + execution
- later timings are usually more representative of steady-state execution

## Benchmarking with `BenchmarkTools`

For more serious timing, the course introduces `@benchmark`.

```julia
@benchmark my_function()
```

The main idea is not memorizing the package syntax. It is recognizing that single-run timing is weak evidence.

## Function Parameters

Julia functions can mix several parameter styles.

Plain positional parameters:

```julia
function my_function(param1, param2)
    param1 + param2
end
```

Default values:

```julia
function my_function(param1, param2 = 2)
    param1 + param2
end
```

## Type-Annotated Parameters

You can restrict accepted argument types directly in the signature.

```julia
function my_function(param1::String, param2::Integer = 2)
    param1 ^ param2
end
```

This is useful when you want stronger contracts or multiple dispatch behavior.

## Keyword Arguments

Keyword arguments are separated with `;`.

```julia
function person(; location)
    println(location)
end
```

You can mix positional and keyword arguments:

```julia
function person(name; location)
    println("$name lives in $location")
end
```

## Varargs

Varargs let a function accept a flexible number of arguments.

```julia
function names(name...)
    println(name)
end
```

You can combine positional arguments, varargs, and keyword arguments in one signature when needed.

## Anonymous Functions

Anonymous functions are short unnamed functions, often used inline.

```julia
(x -> x^2 + 3)(2)
```

They are especially useful for one-off transformation logic.

## `map`

`map(...)` applies a function across each element of a collection.

```julia
map(x -> 2 * x + x^2 + 1, [1, 2, 3])
```

It can also work across multiple input collections:

```julia
map((x, y) -> 2 * x + x^2 + 1 + y, [1, 2, 3], [1, 1, 1])
```

This is a common functional-style Julia pattern.

## More on Multiple Dispatch

Multiple dispatch is not just a beginner novelty. It is a core way Julia scales function behavior.

```julia
function add_values(x, y)
    x + y
end

function add_values(x::String, y::String)
    x * y
end
```

The selected method depends on argument types, not only on function name.

## DataFrame Cleaning

The intermediate material also adds practical tabular cleanup patterns.

Renaming columns:

```julia
rename!(stock_data, Dict(:Adj_Close => :adj_close))
```

Filtering rows:

```julia
filtered = filter(row -> row.Close > 100, stock_data)
```

## Missing Data

Missing values are common in real tabular data.

`describe(...)` helps surface them:

```julia
describe(stock_data)
```

The `nmissing` column in the summary is often the quickest first signal.

## Dropping Missing Rows

```julia
dropmissing!(stock_data, :"Close")
```

This mutates the DataFrame by removing rows with missing values in the chosen column.

That can be useful, but it is not automatically the right statistical choice.

## Replacing Missing Values

```julia
replace!(stock_data[!, "Close"], missing => 130)
```

This fills missing entries with a substitute value.

Important caution: arbitrary imputation is easy to code and easy to misuse.

## Python and R Interop

The course briefly points to:

- `PythonCall`
- `RCall`

These packages let Julia interoperate with Python or R when a needed package or capability is not native to Julia.

The main design lesson is simple:

- stay in Julia when possible
- bridge out when the ecosystem need is real

## Common Traps

- using tuple-like data when you really need a mutable vector or dictionary
- forgetting that tuples and named tuples are immutable
- over-trusting the first `@time` result
- writing many specialized one-off loops where `map` or direct iteration would read better
- using `dropmissing!` without thinking about analysis bias
- adding restrictive type annotations before you know they help the design

## Related Notes

- [Julia Fundamentals](julia-fundamentals.md)
- [Java Performance and Concurrency](java-performance-and-concurrency.md)
