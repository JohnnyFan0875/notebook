# Data Quality with Great Expectations

Great Expectations, often abbreviated `GX`, is a data quality platform for expressing expectations about data, validating new batches, and documenting results for teams.

Key point: `GX` turns data quality from a vague review activity into executable checks that can run repeatedly in notebooks, pipelines, and production validation flows.

## Where Great Expectations Fits

This tool is most useful after a team already knows which quality dimensions matter and wants to enforce them consistently.

| Need | How GX Helps |
| --- | --- |
| Repeatable validation | Turns quality rules into reusable expectations |
| Shared quality language | Stores business assumptions in named suites |
| Pipeline checks | Validates new batches before or after downstream use |
| Human-readable reporting | Publishes validation outcomes through Data Docs |

Tip: Use a plain `data-quality.md` page to define the operating model, then use GX to implement the most important checks in code.

## Core Concepts

The extracted material and the current GX documentation point to a small set of concepts that matter most.

| Concept | Practical Meaning |
| --- | --- |
| Data Context | Main GX entry point for configuration and component management |
| Expectation | A verifiable assertion about data |
| Expectation Suite | A group of expectations for one dataset or one use case |
| Validation Definition | A link between a batch of data and an expectation suite |
| Checkpoint | A reusable object that runs validations and optional actions |
| Data Docs | Human-readable documentation for suites and validation results |

Warning: GX terminology and APIs have changed across versions, so keep the concepts stable and verify exact syntax against the version you are using.

## Data Context

The Data Context is the operational home for a GX deployment.

| Data Context Responsibility | Why It Matters |
| --- | --- |
| Manage data sources | Connects GX to the data you want to validate |
| Store expectation suites | Keeps validation logic versionable and reusable |
| Run or organize validations | Supports repeatable quality checks |
| Access Data Docs and results | Helps teams inspect outcomes and history |

In practice, the Data Context is the place where validation assets stop being ad hoc notebook code and become a shared quality system.

## Expectations

An expectation is a verifiable assertion about data.

Common examples include checks for:

1. null values
2. duplicate values
3. allowed sets or ranges
4. string formatting
5. schema shape
6. unusual distributions

Key point: Expectations are only useful when they encode actual business assumptions, not just generic linting.

## Expectation Suites

Expectation Suites group related checks together so they can be run and maintained as one quality contract.

| Suite Design Choice | Example |
| --- | --- |
| Dataset-oriented suite | Customer master data validation |
| Use-case-oriented suite | Reporting-safe subset for finance dashboards |
| Severity-oriented suite | Critical blocking checks vs advisory checks |

Tip: Keep suites coherent. One suite should describe one stable quality contract rather than every possible check you might ever want.

## Validation Definitions and New Data

Once expectations exist, they need to be applied to specific batches of data.

| Object | Role |
| --- | --- |
| Batch | The concrete data being checked |
| Validation Definition | Associates a batch with an expectation suite |
| Validation Result | The outcome of running that validation |

This makes it easier to rerun the same rules on new incoming data without redefining expectations every time.

## Checkpoints and Actions

Checkpoints help operationalize validation.

| Checkpoint Benefit | Practical Use |
| --- | --- |
| Reusability | Run multiple validations with shared parameters |
| Automation | Trigger follow-up actions based on results |
| Consistency | Standardize how validations are executed across jobs |

Actions can send notifications, update documentation, or integrate with workflow tools after validation completes.

## Data Docs

Data Docs turn quality metadata into readable documentation.

| Data Docs Use | Why It Helps |
| --- | --- |
| Browse expectation suites | Makes validation intent easier to review |
| Inspect validation results | Shows what passed, failed, and changed |
| Share with non-engineers | Gives business and governance teams a readable surface |

Tip: Data Docs are especially valuable when data consumers need visibility into quality without reading pipeline code.

## Common Expectation Patterns

The course material emphasized a few practical expectation families.

### Row-Level Expectations

These are applied to each row independently.

| Check Type | Common Goal |
| --- | --- |
| Missingness | Required values should not be null |
| Type | Values should match the expected type |
| Numeric range | Values should stay within allowed bounds |
| String pattern | Text should match valid formatting rules |

Example expectation names often include:

- `ExpectColumnValuesToNotBeNull`
- `ExpectColumnValuesToBeOfType`
- `ExpectColumnValuesToBeBetween`

### Aggregate-Level Expectations

These summarize behavior across the whole column or dataset.

| Check Type | Common Goal |
| --- | --- |
| Distinct-value set | Only approved categories should appear |
| Unique-value count | Cardinality should stay in an expected range |
| Uniqueness | Key columns should not duplicate |
| Most common value | Dominant categories should remain plausible |

Example expectation names often include:

- `ExpectColumnDistinctValuesToEqualSet`
- `ExpectColumnUniqueValueCountToBeBetween`
- `ExpectColumnValuesToBeUnique`
- `ExpectColumnMostCommonValueToBeInSet`

## A Practical GX Workflow

For notebook or pipeline work, a simple sequence is usually enough:

1. create or load a Data Context
2. define an Expectation Suite for the dataset
3. add expectations that reflect business-critical rules
4. create a Validation Definition for the data to be checked
5. run the validation on a new batch
6. inspect the Validation Result or publish Data Docs
7. wrap repeatable production checks in a Checkpoint

Key point: The value is not in collecting many expectations. The value is in running a small, meaningful set repeatedly on the data that actually matters.

## Example Relationship to Data Quality Dimensions

GX is most effective when its checks are mapped back to business quality dimensions.

| Data Quality Dimension | GX-Friendly Example |
| --- | --- |
| Completeness | Required columns must not be null |
| Validity | Values must belong to an allowed set or format |
| Uniqueness | Primary key values must be unique |
| Consistency | Schema or category expectations stay stable across batches |
| Timeliness | Often handled outside GX, then combined with validation workflows |
| Accuracy | Usually needs external reference comparison or custom logic |

Warning: Not every data quality problem can be solved with built-in expectations alone. Accuracy and business-context checks often need reference data or custom expectations.

## When to Use Great Expectations

GX is a strong fit when:

1. the same datasets are validated repeatedly
2. teams need shared documentation of quality rules
3. validation needs to live inside engineering workflows
4. rule failures should trigger alerts, dashboards, or downstream actions

It is a weaker fit when the problem is mostly one-time exploratory cleanup with no need for repeatable enforcement.

## Minimum Standard for a Useful GX Setup

Before calling a GX deployment useful, you should be able to explain:

1. which expectation suites exist and which datasets they protect
2. which expectations are critical versus advisory
3. how new data is linked to suites through validations
4. which checkpoints or actions operationalize the checks
5. where validation results and Data Docs are reviewed
