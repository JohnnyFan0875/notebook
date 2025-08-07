## Data Manipulation and EDA

Data manipulation refers to the process of transforming, cleaning, restructuring, and enriching raw data into a desired format for analysis.

In **pandas**, data manipulation typically involves working with `DataFrame` and `Series` objects using a rich set of functions and operations.

### Why Is Data Manipulation Important?

Before performing statistical analysis, machine learning, or visualization, you often need to:

- Fix missing or inconsistent values
- Filter or sort records
- Combine datasets
- Compute new variables
- Aggregate or reshape data

### Common Data Manipulation Tasks in pandas

| Category                         | Methods / Functions                                           | Purpose                                     |
| -------------------------------- | ------------------------------------------------------------- | ------------------------------------------- |
| [**Creating**](create-data.md) | `pd.DataFrame()`, `read_csv()`, `read_excel()`, `from_dict()` | Create a new DataFrame from scratch or file |
| [**Subsetting**](subset-data.md) | `loc[]`, `iloc[]`, boolean indexing                           | Filter rows or select columns               |
| [**Sorting**](sort-data.md)      | `sort_values()`, `sort_index()`                               | Reorder data by value or index              |
| [**Modifying**](modify-data.md)            | `assign()`, column arithmetic, `rename()`                     | Create or rename columns                    |
| **Modifying Values**             | item assignment (`df[col][i] = val`, `df.loc[]`, `df.at[]`)   | Change individual cell values               |
| **Handling Missing**             | `isna()`, `fillna()`, `dropna()`                              | Detect and treat missing values             |
| **Aggregating**                  | `groupby()`, `agg()`, `pivot_table()`                         | Compute grouped statistics                  |
| **Combining**                    | `merge()`, `concat()`, `join()`                               | Combine multiple DataFrames                 |
| **Reshaping**                    | `melt()`, `pivot()`, `stack()`, `unstack()`                   | Change data layout                          |
| **Exporting**                    | `to_csv()`, `to_excel()`, `to_pickle()`                       | Save data to file                           |
