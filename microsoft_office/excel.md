# Microsoft Excel

## Functions

### TEXTJOIN

Joins multiple values from a range or array into a single text string.

```excel
=TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)
```

- `ignore_empty`: Set to TRUE/FALSE to ignore/include empty cells.
- example: `=TEXTJOIN(",", TRUE, A1:A100)`

### VLOOKUP

Searches for a value in the first column of a range and returns a value from another column in the same row.

```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

- `lookup_value`: The value to search for in the first column of table_array.
- `table_array`: The range of cells that contains the data.
- `col_index_num`: The column number (starting from 1) in the table from which to retrieve the value.
- `range_lookup`: Optional. Use FALSE for an exact match, TRUE (or omitted) for an approximate match.
- example:
  ```
  =VLOOKUP("test", A1:D10, 2, FALSE)
  =VLOOKUP(A11, A1:D10, 2, FALSE)
  ```

### Count `delimiter`-Separated Elements in a Cell

Calculates how many values are separated by delimiter (comma for example) in a single cell.

```excel
=IF(A1<>"", LEN(A1) - LEN(SUBSTITUTE(A1, ",", "")) + 1, "empty")
```

- if A1 cell is empty, return `empty`
- `LEN(A1)`: number of characters in A1 cell
- `LEN(SUBSTITUTE(A1, ",", ""))`: number of characters excluding comma in A1 cell
- `LEN(A1) - LEN(SUBSTITUTE(A1, ",", "")) + 1`: number of comma +1 = number of elements splitted by comma
