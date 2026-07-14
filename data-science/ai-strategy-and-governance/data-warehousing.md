# Data Warehousing

Data warehousing is the practice of collecting, integrating, organizing, and storing data so that it can support large-scale analysis, reporting, and decision-making across an organization.

Key point: A data warehouse is not just a bigger database. It is designed for analytical workloads, integrated business views, and historical reporting rather than day-to-day transaction processing.

## What a Data Warehouse Does

A warehouse gathers data from multiple operational sources and makes it available for analysis in a form that is more consistent and easier to query.

| Warehouse Function | Why It Matters |
| --- | --- |
| Collect data from many systems | Brings fragmented operational data into one analytical environment |
| Integrate and standardize | Makes cross-functional analysis possible |
| Preserve historical context | Supports trend analysis, reporting, and business review |
| Enable BI and analytics | Gives analysts and decision-makers a stable reporting layer |

Tip: Warehouses create value by reducing the effort needed to answer recurring business questions across teams.

## Data Warehouse vs Database vs Data Mart vs Data Lake

These systems solve related but different problems.

| System | Main Purpose | Typical Data Shape |
| --- | --- | --- |
| Transactional database | Run operational applications and store transactions | Structured, row-oriented |
| Data warehouse | Support organization-wide analytics and reporting | Structured, integrated, analytical |
| Data mart | Support analysis for a narrower subject area or department | Structured, focused |
| Data lake | Store large volumes of raw or varied data for flexible future use | Structured and unstructured |

Key point: Warehouses emphasize known analytical use cases and organized structure, while lakes emphasize flexible storage and broader raw-data coverage.

## Why Organizations Use Data Warehouses

Warehouses are especially useful when organizations need analysis without burdening transactional systems.

Common reasons include:

1. support BI and reporting
2. improve organizational decision-making
3. avoid slowing down operational databases with large analytical queries
4. create a stable basis for forecasting, compliance analysis, and growth planning

## Typical Warehouse Layers

Many warehouse architectures can be described with a layered model.

| Layer | Role |
| --- | --- |
| Data source layer | Operational systems, logs, files, spreadsheets, and other inputs |
| Data staging layer | Extraction, transformation, validation, and temporary preparation area |
| Data storage layer | Warehouse tables and sometimes downstream data marts |
| Data presentation layer | BI tools, dashboards, data mining tools, and direct analytical queries |

Tip: The staging layer is where much of the messy integration work happens so that the presentation layer can stay simpler and more reliable.

## Presentation Layer Users and Tools

The presentation layer exists for people, not just systems.

| Tool Group | Typical Use |
| --- | --- |
| Automated reporting and dashboards | Recurring metrics, KPIs, executive and operational reporting |
| BI and analytics tools | Exploratory analysis and pattern discovery |
| Direct queries | Advanced analysis by analysts, data scientists, or engineers |

## Warehouse Life Cycle

A warehouse is typically developed and maintained through a recurring life cycle.

| Life Cycle Area | Typical Activities |
| --- | --- |
| Planning | Clarify business requirements and reporting needs |
| Data modeling | Design fact tables, dimensions, and grain |
| Implementation | Build ETL or ELT pipelines and BI interfaces |
| Maintenance | Modify, test, deploy, and support the system over time |

Key point: Warehouses are not one-time builds. They are long-lived analytical products that require ongoing maintenance and evolution.

## Inmon vs Kimball

Two classic design philosophies appear often in data warehousing.

| Approach | Main Idea | Trade-off |
| --- | --- | --- |
| Inmon, top-down | Build an integrated enterprise warehouse first, then derive marts | More upfront design effort, stronger enterprise consistency |
| Kimball, bottom-up | Start with dimensional data marts and grow from business processes | Faster delivery, lower startup cost, but more coordination needed over time |

### Inmon, Top-Down

This approach prioritizes an enterprise-level integrated design before broad consumption.

| Advantage | Disadvantage |
| --- | --- |
| Strong single source of truth | Lengthy upfront work |
| Easier to align downstream marts later | Higher startup cost |

### Kimball, Bottom-Up

This approach starts from concrete business processes and delivers dimensional models early.

| Advantage | Disadvantage |
| --- | --- |
| Faster initial delivery | More ETL coordination over time |
| Lower upfront cost | Greater risk of duplication if domains drift apart |

Tip: Kimball is often attractive when a team needs to prove business impact quickly.

## Fact Tables and Dimension Tables

Dimensional modeling is central to many warehouses.

| Table Type | Purpose |
| --- | --- |
| Fact table | Stores measurable events or metrics such as sales, units, or revenue |
| Dimension table | Stores descriptive context such as customer, product, date, or location |

Fact tables usually contain numeric measures and foreign keys. Dimension tables provide the descriptive fields that make those measures interpretable.

Key point: Facts answer "how much" or "how many." Dimensions answer "by whom, when, where, what, or under which category."

## Star and Snowflake Schemas

The most common dimensional layouts are star and snowflake schemas.

| Schema | Practical Meaning |
| --- | --- |
| Star schema | One central fact table linked directly to dimension tables |
| Snowflake schema | Dimensions are further normalized into related sub-dimensions |

Star schemas are usually easier for business users to understand. Snowflake schemas can reduce redundancy but make joins and browsing more complex.

## Kimball Modeling Steps

The extracted material follows a common Kimball-style dimensional design sequence.

1. select the organizational process
2. declare the grain
3. identify the dimensions
4. identify the facts

### 1. Select the Organizational Process

Start from a business process such as billing, purchases, marketing, or product monitoring.

### 2. Declare the Grain

Grain defines the lowest level each fact row represents.

Warning: If grain is vague or inconsistent, every downstream metric becomes harder to trust.

### 3. Identify the Dimensions

Choose the descriptive fields users need to analyze the process, such as time, customer, product, location, or payment method.

### 4. Identify the Facts

Choose the numeric measures that are true at the selected grain, such as sales amount, units sold, or time spent before purchase.

## Slowly Changing Dimensions

Dimension values change over time, and warehouses need a policy for how to handle that history.

| Type | Behavior | Trade-off |
| --- | --- | --- |
| Type I | Overwrite the old value | Simple, but historical value is lost |
| Type II | Add a new row for the changed version | Preserves history, but adds complexity |
| Type III | Add columns for current and prior value | Limited history, simpler than full row versioning |
| Snapshot approach | Periodically snapshot full dimension state | Useful for broader historical reporting |

Key point: Slowly changing dimensions are really business decisions about history, not only technical table patterns.

## OLAP vs OLTP

Warehouses are commonly associated with `OLAP`, while operational systems are commonly `OLTP`.

| Characteristic | OLAP | OLTP |
| --- | --- | --- |
| Main purpose | Analysis | Transaction processing |
| Query style | Complex, read-heavy, multi-dimensional | Simple, frequent, write-heavy |
| Data organization | Often dimensional or analytical | Rows and columns for operations |
| Typical system role | Reporting and analytics | Source systems and applications |

Tip: Moving analytical work into a warehouse helps keep OLTP systems responsive for operational traffic.

## Row Store vs Column Store

Analytical warehouses often benefit from column-oriented storage.

| Storage Style | Best Fit |
| --- | --- |
| Row store | Transactional workloads where full rows are accessed together |
| Column store | Analytical workloads where queries scan a few columns over many rows |

Column stores often improve analytical performance and compression because related column values are stored together.

## ETL vs ELT

Both are ways to move data into an analytical environment, but the order of operations differs.

| Pattern | Sequence |
| --- | --- |
| ETL | Extract -> Transform -> Load |
| ELT | Extract -> Load -> Transform |

### ETL

| ETL Strength | ETL Limitation |
| --- | --- |
| Lower warehouse storage needs | Transformation fixes may require re-pulling data |
| Can help with PII handling before loading | Often needs separate processing infrastructure |

### ELT

| ELT Strength | ELT Limitation |
| --- | --- |
| Transformations can be rerun from loaded raw data | Raw-data storage needs are higher |
| Fits cloud scaling and near real-time needs well | Privacy and compliance controls must be carefully enforced inside the warehouse |

Key point: ELT becomes more attractive when cloud platforms make storage and compute scalable, but ETL can still be useful when early transformation or stricter pre-load control is needed.

## Data Cleaning in Warehouse Pipelines

Warehouse quality depends heavily on data cleaning in the pipeline.

| Cleaning Task | Purpose |
| --- | --- |
| Format normalization | Standardize dates, categories, and capitalization |
| Address parsing | Split and validate address fields into components |
| Validation | Check ranges, types, and business-rule compliance |
| De-duplication | Remove repeated records that distort analysis |

Tip: A warehouse can only be as trustworthy as the rules used to clean and validate the incoming data.

## On-Premise, Cloud, and Hybrid Deployment

Warehouses can be deployed in different infrastructure models.

| Model | Strength | Main Trade-off |
| --- | --- | --- |
| On-premise | High control and custom optimization | High upfront cost and more maintenance burden |
| Cloud | Fast scaling and less infrastructure maintenance | Less low-level control and potentially variable cost |
| Hybrid | Useful for backup, recovery, or mixed constraints | Operational complexity increases |

## Choosing a Practical Approach

Real warehouse design choices depend on business context.

Useful decision questions include:

1. do we need fast visible business impact or a longer enterprise foundation
2. do we expect raw data to be retained for reprocessing
3. is cloud scalability more valuable than infrastructure control
4. which business process should be modeled first
5. which history policy is required for changing dimensions

Warning: There is no single best warehouse design. The right choice depends on workload, team size, governance needs, and time-to-value expectations.

## Minimum Standard for a Usable Warehouse Design

Before calling a warehouse design credible, you should be able to explain:

1. which business processes the warehouse supports
2. which source systems feed it and how the layers interact
3. which dimensional model, grain, facts, and dimensions were chosen
4. whether ETL or ELT is being used and why
5. how the design supports analytical performance, quality, and maintainability
