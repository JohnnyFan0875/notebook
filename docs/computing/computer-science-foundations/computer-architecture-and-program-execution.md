# Computer Architecture and Program Execution

## Why This Matters

Programs only become useful when their instructions can be represented in a form the machine can execute. A practical mental model is:

`human intent -> source code -> translation layer -> machine instructions -> hardware execution`

This helps explain why abstraction layers matter in programming, performance, debugging, and systems design.

## Main Components of a Computer

| Component | Main role | Typical questions |
| --- | --- | --- |
| CPU | Executes instructions and coordinates work | What operation is performed next? |
| Memory (RAM) | Stores active data and instructions | What is needed right now? |
| Storage | Keeps data persistently | What must survive after shutdown? |
| Input | Brings information into the system | What does the computer receive? |
| Output | Presents results | What does the computer produce? |

## CPU Execution Cycle

The central simplified model is the fetch-decode-execute cycle:

1. Fetch an instruction from memory.
2. Decode what operation it represents.
3. Execute the operation.
4. Store or expose the result, then continue.

Even high-level programs eventually reduce to repeated low-level instruction execution.

## Why Binary Is the Common Representation

Computers use binary because physical hardware can reliably distinguish between two stable states. In practice, this means:

- Data is encoded as bits.
- Instructions are also encoded as bits.
- Arithmetic, storage, and logic all operate on these binary representations.

Two useful habits:

- Read binary as positional notation with powers of two.
- Separate the representation from the meaning. The same bit pattern might be interpreted as an integer, character, color value, or instruction depending on context.

## Binary Conversion Intuition

### Binary to Decimal

Expand each bit by its positional value and sum the results.

Example:

`1011_2 = 1*2^3 + 0*2^2 + 1*2^1 + 1*2^0 = 11`

### Decimal to Binary

Repeatedly divide by 2 and track remainders, or choose the largest powers of two that fit the number.

## From Programs to Machine Execution

Programming languages sit between human reasoning and hardware execution.

| Layer | Role |
| --- | --- |
| High-level language | Expresses logic in a human-friendly form |
| Translator | Converts source code into executable steps |
| Machine code / lower-level representation | Form the CPU can act on directly |

## Compilation vs Interpretation

### Compilation

- Translates the program ahead of execution into a lower-level form.
- Often improves runtime efficiency.
- Errors are commonly caught before execution starts.

### Interpretation

- Executes the program through an intermediary at runtime.
- Often improves iteration speed and flexibility.
- Runtime behavior depends more directly on the interpreter environment.

In real systems the boundary is not absolute. Many modern runtimes combine compilation, interpretation, bytecode, and just-in-time optimization.

## Practical Takeaways

- Hardware executes instructions, not source code.
- Binary is the machine-level representation that makes digital execution possible.
- Translation layers explain why languages differ in speed, portability, and tooling.
- Understanding the execution path helps when reasoning about performance, memory use, and debugging.
