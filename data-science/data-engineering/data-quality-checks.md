# Data Quality Checks

Data quality is the practice of ensuring that data is fit for its intended business use through defined dimensions, rules, monitoring, and remediation processes.

This note focuses on **organization-level data quality operations**: dimensions, rules, monitoring, ownership, and remediation. If you are cleaning a dataset before analysis, start with [Statistics: Data Quality](../statistics/descriptive-statistics/data-quality.md).

Key point: Data quality is not only about cleaning bad rows. It is an operating discipline that connects business expectations, technical validation, alerting, and accountable issue resolution.

## Why Data Quality Matters

Organizations use data for reporting, operations, compliance, and AI, but poor-quality data quietly weakens all of them.

| Data Quality Outcome | Why It Matters |
| --- | --- |
| Better decisions | Reports and models are less likely to be distorted |
| Safer operations | Downstream processes fail less often because of missing or invalid data |
| Stronger trust | Users are more willing to rely on governed data assets |
| Faster issue resolution | Known rules and ownership reduce confusion when problems appear |

Tip: The business value of data quality often appears indirectly through fewer escalations, less rework, and more credible reporting.

## Activities for Good Data Quality

Data used for decisions and business processes should meet a small set of operational expectations.

| Activity | Practical Meaning |
| --- | --- |
| Monitoring | Data is checked continuously instead of only during one-time cleanup |
| Timely issue resolution | Problems have a defined path to remediation |
| Shared understanding | Producers and consumers understand how quality is defined |
| Ongoing process | Quality work is repeated as data, systems, and use cases change |

Key point: A data quality process is continuous because new source changes, business rules, and downstream uses keep creating new failure modes.

## Core Data Quality Dimensions

A common way to make quality measurable is to define dimensions that describe what "fit for purpose" means.

| Dimension | Practical Definition | Example Question |
| --- | --- | --- |
| Completeness | Expected records or fields are present | Are all customer records loaded, and are required fields populated? |
| Validity | Values meet allowed formats, ranges, or business criteria | Is the birth date in a valid format and logically possible? |
| Uniqueness | Records that should be unique are not duplicated | Does each customer have one true identifier? |
| Consistency | Related values agree across records or systems | Does a referenced customer ID also exist in the customer table? |
| Timeliness | Data arrives when it is needed | Was the daily dataset loaded before the reporting cutoff? |
| Accuracy | Data matches reality or an accepted source of truth | Does the address match the verified tax form? |

### Completeness

Completeness can be measured at both the dataset level and the data-element level.

| Level | Meaning |
| --- | --- |
| Dataset level | All expected records are present |
| Data element level | Required fields are populated when expected |

Business issues from poor completeness often include skewed reporting and direct customer impact.

### Validity

Validity asks whether values satisfy business and technical rules.

| Validity Need | Example |
| --- | --- |
| Allowed format | Date must follow a required pattern |
| Allowed domain | Account status must be `Open`, `Closed`, or `Pending` |
| Logical correctness | A birth date must be in the past |

Tip: Validity almost always requires business context. A technically well-formed value can still be invalid for the process.

### Uniqueness

Uniqueness protects data from duplicated entities and events.

| Uniqueness Check | Example |
| --- | --- |
| Single-key uniqueness | Customer ID must be unique |
| Composite uniqueness | Name, birth date, and address together should not repeat unexpectedly |

### Consistency

Consistency checks whether data agrees across systems, records, and time.

| Consistency Check | Example |
| --- | --- |
| Cross-table agreement | Account table customer IDs must exist in the customer table |
| Volume consistency | Today's load count should stay within an expected range of yesterday's load |

### Timeliness

Timeliness measures whether data is available early enough for the business use case.

| Timeliness Check | Example |
| --- | --- |
| Dataset timeliness | Daily customer data must load by `9:00 AM` |
| Element timeliness | Tax ID must be populated by the time an account becomes `Open` |

Warning: Data can be complete and valid but still operationally useless if it arrives too late.

### Accuracy

Accuracy compares stored values to a trusted reference or real-world condition.

| Accuracy Check | Example |
| --- | --- |
| External source comparison | Customer identity fields match a tax form |
| Verified reference comparison | Stored address matches the approved source record |

## Data Quality Rules

A data quality rule is a business rule that validates whether data meets requirements.

| Rule Scope | Meaning |
| --- | --- |
| Dataset level | Checks the dataset as a whole, such as record counts or arrival time |
| Data element level | Checks field-level expectations, such as required values or valid formats |

Key point: Good data quality rules translate vague expectations like "clean data" into conditions that can actually be tested.

## Example Rules by Dimension

| Dimension | Dataset-Level Example | Data-Element Example |
| --- | --- | --- |
| Completeness | All expected source records must load into the target table | All records must have `Customer ID`, `Customer Name`, and `Account Type` populated |
| Validity | None required in every case | `Birth Date` must be valid and in the past; `Account Status` must be in an allowed list |
| Uniqueness | None required in every case | `Customer ID` must be unique |
| Consistency | Today's record count must be within `+/- 5%` of yesterday's | All `Customer ID` values in the account table must exist in the customer table |
| Timeliness | Daily customer data must load by `9:00 AM` | Tax ID must be populated before an account is first marked `Open` |
| Accuracy | Often measured through reconciliation | Customer profile fields must match a trusted source document |

## Detective vs Preventative Rules

Not every quality problem should be handled the same way.

| Rule Type | Purpose | Typical Behavior |
| --- | --- | --- |
| Detective rule | Monitor data after it has been loaded downstream | Alert, investigate, and remediate |
| Preventative rule | Stop bad data from moving further in the pipeline | Block loading until the issue is addressed |

### When Detective Rules Make Sense

Detective rules are useful when:

1. the issue will not cause significant harm if it is not fixed immediately
2. the issue is too complex to remediate quickly
3. the issue affects a relatively small number of records

### When Preventative Rules Make Sense

Preventative rules are useful when:

1. the data is critical to business processes and an issue would cause immediate harm
2. the issue can be fixed quickly
3. the issue affects a large number of records

Tip: Detect first when learning, prevent later when the business impact and remediation path are both clear.

## Anomaly Detection for Data Quality

Rule-based checks are not the only option. Some teams use anomaly detection to identify unexpected quality problems at scale.

| Benefit | Why It Helps |
| --- | --- |
| Scale | Can monitor more data than a small manual ruleset |
| Lower setup friction | Requires less explicit business-rule specification at the start |
| Drift detection | Can surface pattern changes that fixed thresholds miss |

Anomaly detection is most useful when large amounts of data need monitoring and manual review alone no longer scales.

Warning: Anomaly detection helps find suspicious patterns, but it does not replace business-defined rules for critical controls.

## Thresholds and Alerts

Rules become operational only when teams decide what level of failure should trigger action.

| Concept | Meaning |
| --- | --- |
| Alert threshold | A count or percentage limit for rule failures |
| Alert owner | Usually the data producer, consumer, or both |
| Trigger | Action starts when failures exceed the allowed threshold |

Thresholds should reflect the criticality, priority, and impact of the issue. More critical fields usually require stricter thresholds.

### Common Alert Levels

| Level | Meaning | Typical Response |
| --- | --- | --- |
| Level 1: Warning | Threshold breached but no rapid remediation required | Monitor and plan cleanup |
| Level 2: Critical issue alert | Threshold breached and rapid remediation required | Escalate and fix quickly |
| Level 3: Critical issue prevent | Threshold breached and downstream movement should stop | Block the pipeline or release |

Key point: Threshold design is a business decision as much as a technical one, because it decides which defects are tolerable and which are not.

## Roles and Responsibilities

Data quality work usually spans producers, consumers, and governance functions.

| Role | Typical Responsibilities |
| --- | --- |
| Data producer | Implement rules, own technical fixes, and remediate issues in source or pipeline logic |
| Data consumer | Recommend rules, understand data fitness before use, and report issues |
| Data governance team | Define policy, clarify roles, monitor dashboards, and ensure tools and training exist |

Tip: Many people are both producers and consumers at different points in the same pipeline, so ownership should be explicit for each handoff.

## A Practical Remediation Flow

One useful operating pattern is:

1. a consumer identifies a quality issue or a missing rule
2. the producer implements or updates the rule and remediates the issue
3. the governance function oversees the process and tracks it in dashboards

This keeps quality from becoming either "only a business complaint" or "only an engineering cleanup."

## Minimum Standard for a Healthy Data Quality Practice

Before calling a data quality practice operational, you should be able to explain:

1. which quality dimensions matter for the dataset and why
2. which dataset-level and element-level rules are enforced
3. when the pipeline should detect issues versus prevent downstream loading
4. how thresholds and alerts are set by criticality
5. who owns remediation, escalation, and monitoring

## Executable Checks with Great Expectations

Great Expectations, often abbreviated `GX`, is a data quality platform for expressing expectations about data, validating new batches, and documenting results for teams.

Key point: `GX` turns data quality from a vague review activity into executable checks that can run repeatedly in notebooks, pipelines, and production validation flows.

### Where Great Expectations Fits

This tool is most useful after a team already knows which quality dimensions matter and wants to enforce them consistently.

| Need | How GX Helps |
| --- | --- |
| Repeatable validation | Turns quality rules into reusable expectations |
| Shared quality language | Stores business assumptions in named suites |
| Pipeline checks | Validates new batches before or after downstream use |
| Human-readable reporting | Publishes validation outcomes through Data Docs |

Tip: Use a plain `data-quality.md` page to define the operating model, then use GX to implement the most important checks in code.

### Core Concepts

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

### Data Context

The Data Context is the operational home for a GX deployment.

| Data Context Responsibility | Why It Matters |
| --- | --- |
| Manage data sources | Connects GX to the data you want to validate |
| Store expectation suites | Keeps validation logic versionable and reusable |
| Run or organize validations | Supports repeatable quality checks |
| Access Data Docs and results | Helps teams inspect outcomes and history |

In practice, the Data Context is the place where validation assets stop being ad hoc notebook code and become a shared quality system.

### Expectations

An expectation is a verifiable assertion about data.

Common examples include checks for:

1. null values
2. duplicate values
3. allowed sets or ranges
4. string formatting
5. schema shape
6. unusual distributions

Key point: Expectations are only useful when they encode actual business assumptions, not just generic linting.

### Expectation Suites

Expectation Suites group related checks together so they can be run and maintained as one quality contract.

| Suite Design Choice | Example |
| --- | --- |
| Dataset-oriented suite | Customer master data validation |
| Use-case-oriented suite | Reporting-safe subset for finance dashboards |
| Severity-oriented suite | Critical blocking checks vs advisory checks |

Tip: Keep suites coherent. One suite should describe one stable quality contract rather than every possible check you might ever want.

### Validation Definitions and New Data

Once expectations exist, they need to be applied to specific batches of data.

| Object | Role |
| --- | --- |
| Batch | The concrete data being checked |
| Validation Definition | Associates a batch with an expectation suite |
| Validation Result | The outcome of running that validation |

This makes it easier to rerun the same rules on new incoming data without redefining expectations every time.

### Checkpoints and Actions

Checkpoints help operationalize validation.

| Checkpoint Benefit | Practical Use |
| --- | --- |
| Reusability | Run multiple validations with shared parameters |
| Automation | Trigger follow-up actions based on results |
| Consistency | Standardize how validations are executed across jobs |

Actions can send notifications, update documentation, or integrate with workflow tools after validation completes.

### Data Docs

Data Docs turn quality metadata into readable documentation.

| Data Docs Use | Why It Helps |
| --- | --- |
| Browse expectation suites | Makes validation intent easier to review |
| Inspect validation results | Shows what passed, failed, and changed |
| Share with non-engineers | Gives business and governance teams a readable surface |

Tip: Data Docs are especially valuable when data consumers need visibility into quality without reading pipeline code.

### Common Expectation Patterns

The course material emphasized a few practical expectation families.

#### Row-Level Expectations

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

#### Aggregate-Level Expectations

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

### A Practical GX Workflow

For notebook or pipeline work, a simple sequence is usually enough:

1. create or load a Data Context
2. define an Expectation Suite for the dataset
3. add expectations that reflect business-critical rules
4. create a Validation Definition for the data to be checked
5. run the validation on a new batch
6. inspect the Validation Result or publish Data Docs
7. wrap repeatable production checks in a Checkpoint

Key point: The value is not in collecting many expectations. The value is in running a small, meaningful set repeatedly on the data that actually matters.

### Example Relationship to Data Quality Dimensions

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

### When to Use Great Expectations

GX is a strong fit when:

1. the same datasets are validated repeatedly
2. teams need shared documentation of quality rules
3. validation needs to live inside engineering workflows
4. rule failures should trigger alerts, dashboards, or downstream actions

It is a weaker fit when the problem is mostly one-time exploratory cleanup with no need for repeatable enforcement.

### Minimum Standard for a Useful GX Setup

Before calling a GX deployment useful, you should be able to explain:

1. which expectation suites exist and which datasets they protect
2. which expectations are critical versus advisory
3. how new data is linked to suites through validations
4. which checkpoints or actions operationalize the checks
5. where validation results and Data Docs are reviewed
