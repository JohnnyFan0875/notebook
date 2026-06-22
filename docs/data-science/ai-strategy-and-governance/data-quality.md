# Data Quality

Data quality is the practice of ensuring that data is fit for its intended business use through defined dimensions, rules, monitoring, and remediation processes.

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
