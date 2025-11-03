# Study Designs in Epidemiology and Clinical Research

## Study Designs

Study designs are broadly divided into three main categories:

1. **Observational studies** – researchers do not intervene, only observe.
2. **Experimental studies** – researchers assign interventions.
3. **Evidence synthesis** – researchers summarize findings across multiple studies.

## Hierarchy

```
Study Designs
├── Observational
│   ├── Cohort
│   │   ├── Prospective
│   │   └── Retrospective
│   ├── Case–Control
│   ├── Cross-Sectional
│   └── Longitudinal
├── Experimental
│   ├── Randomized Controlled Trial (RCT)
│   ├── Experimental Design
│   ├── Explanatory Design
│   ├── Descriptive Design
│   └── Correlational Design
└── Evidence Synthesis
    ├── Systematic Review
    └── Meta-analysis

```

## 1. Observational Studies

Researchers observe exposures and outcomes without intervention.
Includes **Cohort**, **Case–Control**, and **Cross-Sectional** studies.

### 1.1 Cohort Studies

- Participants are grouped by **exposure status** (exposed vs. unexposed), then followed to determine outcomes.
- Key feature: Exposure identified **before** outcome.

#### a. Prospective Cohort

- Researchers enroll participants now and follow them forward in time.
- Often start with healthy individuals who are free from the disease or outcome of interest
- **Example:** The _Framingham Heart Study_ (since 1948) has followed residents to identify cardiovascular risk factors (e.g., smoking, cholesterol, blood pressure).
- **Strengths:** Clear temporal sequence, less recall bias.
- **Weaknesses:** Time- and cost-intensive.

![Image](https://www.scribbr.com/wp-content/uploads/2023/06/prospective-cohort-study.webp)

#### b. Retrospective Cohort

- Researchers use **existing records** (e.g., medical charts, registries) to reconstruct past exposures and outcomes.
- **Example:** Hospital employee vaccination records linked to archived infection data.
- **Strengths:** Faster, less expensive.
- **Weaknesses:** Data quality limits, missing confounders.

![Image](https://www.scribbr.co.uk/wp-content/uploads/2023/06/retrospective-cohort-study.webp)

### 1.2 Case–Control Studies

- Start with **outcome status**:

  - Cases = individuals with disease/outcome
  - Controls = individuals without disease

- Look backward to assess exposures.
- **Example:** Doll & Hill (1950s) showed smoking was strongly associated with lung cancer by comparing smoking history of lung cancer patients vs. controls.
- **Strengths:** Efficient for rare diseases, multiple exposures.
- **Weaknesses:** Recall bias, cannot directly measure incidence (case–control starts with outcome, not population at risk).

### 1.3 Cross-Sectional Studies

- Snapshot of exposure and outcome measured **at the same time**.
- **Example:** The CDC conducts annual telephone surveys of thousands of adults, collecting data at one point in time on smoking, alcohol use, physical activity, obesity, and chronic disease prevalence.
- **Strengths:** Quick, inexpensive, useful for prevalence estimates.
- **Weaknesses:** No temporal sequence, cannot infer causality.

### 1.4 Longitudinal Studies

- Track the same participants over an extended period, collecting data at multiple time points.
- Can be **prospective** (follow forward) or **retrospective** (using past records).
- Unlike cross-sectional studies, longitudinal designs establish **temporal relationships** between exposure and outcome.

**Examples:**

- The Nurses’ Health Study (since 1976) following >100,000 women to examine diet, lifestyle, and chronic disease.
- Long-term school-based studies assessing how early-life factors affect adult outcomes.

**Strengths:**

- Can observe **changes over time** within individuals.
- Establishes temporal sequence (exposure precedes outcome).
- Useful for incidence, risk factor identification, and natural history of disease.

**Weaknesses:**

- Time- and cost-intensive.
- Attrition bias (participants dropping out).
- Requires strong data management and follow-up.

![Image](https://www.questionpro.com/blog/wp-content/uploads/2018/06/cross-sectional-study-vs-longitudinal-study-min-scaled-1.jpg)

## 2. Experimental Studies

Researchers intervene and randomly assign participants to groups.

### 2.1 Randomized Controlled Trial (RCT)

- Participants are randomly assigned to intervention vs. control groups.
- **Example:** The _Women’s Health Initiative (WHI)_ hormone therapy trial tested estrogen/progesterone vs. placebo in postmenopausal women, showing increased breast cancer and cardiovascular risk.
- **Strengths:** Gold standard for causal inference, minimizes bias.
- **Weaknesses:** Expensive, ethical constraints, may lack generalizability.

![Image](https://www.simplypsychology.org/wp-content/uploads/randomized-controlled-trial-1536x894.jpeg)

### 2.2 Experimental Design

- Involves deliberate manipulation of one or more independent variables to measure their effect on dependent variables.
- Often includes control groups, randomization, and replication.
- **Example:** Testing different doses of a new drug on separate patient groups.
- **Strengths:** Establishes causality.
- **Weaknesses:** May be difficult or unethical in human studies.

### 2.3 Explanatory Design

- Focuses on explaining the relationships or mechanisms underlying observed phenomena.
- Goes beyond description to identify causal links.
- **Example:** Examining how exercise reduces blood pressure through changes in vascular function.
- **Strengths:** Provides mechanistic insights.
- **Weaknesses:** Requires strong theoretical framework and careful control of confounding variables.

### 2.4 Descriptive Design

- Aims to describe characteristics of a population or phenomenon.
- Does not test hypotheses but provides valuable baseline data.
- **Example:** Describing demographic patterns of diabetes prevalence in a region.
- **Strengths:** Useful for generating hypotheses and informing policy.
- **Weaknesses:** Cannot establish causality.

### 2.5 Correlational Design

- Examines the relationship between two or more variables without manipulation.
- Determines whether variables are associated (positive, negative, or no correlation).
- **Example:** Investigating the association between physical activity and depression scores.
- **Strengths:** Identifies potential associations.
- **Weaknesses:** Correlation does not imply causation.

## 3. Evidence Synthesis

Researchers summarize and analyze findings from multiple studies.

### 3.1 Systematic Review

- Comprehensive collection and critical evaluation of all relevant studies.
- **Example:** Cochrane systematic reviews of vaccines or cancer therapies.

### 3.2 Meta-Analysis

- Statistical pooling of results from multiple studies (often nested within a systematic review).
- **Example:** Meta-analysis of statin RCTs showing reduction in cardiovascular mortality.
- **Strengths:** Provides higher-level evidence, increases power.
- **Weaknesses:** Limited by quality and heterogeneity of included studies.

## 4. Summary Table

| Category               | Study type             | Direction            | Key feature                                | Example                               |
| ---------------------- | ---------------------- | -------------------- | ------------------------------------------ | ------------------------------------- |
| **Observational**      | Cohort (prospective)   | Forward              | Exposure → outcome (future follow-up)      | Framingham Heart Study                |
|                        | Cohort (retrospective) | Backward (records)   | Exposure → outcome (archived data)         | Hospital vaccination vs. infection    |
|                        | Case–control           | Backward             | Start with outcome, look for exposures     | Doll & Hill smoking–lung cancer study |
|                        | Cross-sectional        | Snapshot             | Exposure & outcome measured simultaneously | NHANES obesity surveys                |
| **Experimental**       | RCT                    | Forward (random)     | Randomized intervention vs. control        | WHI hormone therapy trial             |
|                        | Experimental design    | Forward (controlled) | Manipulation of independent variables      | Drug dose testing                     |
|                        | Explanatory design     | Forward              | Explains causal mechanisms                 | Exercise and vascular function        |
|                        | Descriptive design     | Snapshot             | Describes population characteristics       | Diabetes prevalence                   |
|                        | Correlational design   | Snapshot             | Examines associations between variables    | Physical activity vs. depression      |
| **Evidence synthesis** | Systematic review      | N/A                  | Critical synthesis of multiple studies     | Cochrane vaccine review               |
|                        | Meta-analysis          | N/A                  | Statistical pooling of study results       | Statin RCT meta-analysis              |

## 5. Genetic Association and Clinical Endpoint Analysis

Beyond classical epidemiologic study designs, clinical research often requires appropriate statistical methods to evaluate genetic variants (e.g., germline SNPs) in relation to different endpoints. The following summarizes typical analysis strategies:

### A. Incidence (Disease Risk Analysis)

- **Control group:** Healthy individuals without cancer.
- **Methods:**

  - Chi-square test: initial comparison of SNP distribution.
  - Logistic regression: association between SNP and incidence, adjusting for demographic covariates (age, sex, etc.).
  - ROC curve: evaluate the discriminative ability of SNPs to classify cases vs. controls.

### B. Treatment Response Analysis

- **Variables:** Specific therapies (chemotherapy, targeted therapy, radiotherapy).
- **Methods:**

  - Chi-square test: SNP vs. binary treatment response (responder/non-responder).
  - Logistic regression: adjusted for age, sex, and stage, to assess SNP as an independent predictor.
  - ROC curve: assess predictive performance.

### C. Recurrence Risk Analysis

- **Required data:** Recurrence status and follow-up time → definition of Disease-Free Survival (DFS).
- **Starting time:** Surgery or treatment initiation.
- **Methods:**

  - Chi-square test: initial proportion comparison.
  - Cox regression: adjusted analysis of SNP effect on DFS.
  - Kaplan–Meier survival curve: visualize survival differences by SNP genotype.
  - ROC curve: evaluate discriminatory ability.

### D. Mortality Risk Analysis

- **Required data:** Survival status and follow-up time; exclude non-disease deaths.
- **Starting time:** Surgery or treatment initiation.
- **Methods:**

  - Chi-square test: crude mortality proportion comparison.
  - Cox regression: adjusted hazard ratios for SNP and overall survival (OS).
  - Kaplan–Meier survival curve: survival probability comparison by genotype.
  - ROC curve: predictive performance assessment.
