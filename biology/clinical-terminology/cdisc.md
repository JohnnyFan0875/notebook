# CDISC SDTM / ADaM

## 1. Overview

**CDISC** (Clinical Data Interchange Standards Consortium) develops global standards that streamline the collection, organization, analysis, and regulatory submission of **clinical trial data**. These standards ensure that data from clinical studies are **consistent, machine-readable, and compliant** with regulatory requirements (e.g., FDA, EMA).

Two of the most widely used CDISC models are:

- **SDTM (Study Data Tabulation Model)** – for organizing raw clinical trial data.
- **ADaM (Analysis Data Model)** – for preparing data used in statistical analyses.

## 2. SDTM (Study Data Tabulation Model)

### Purpose

SDTM defines how clinical trial data should be **structured for regulatory submission**. It converts collected clinical data into standardized **domains** for consistency across studies.

### Structure

Each SDTM dataset represents a domain (subject area) organized by variables.

| Domain | Description      | Example Variables             |
| ------ | ---------------- | ----------------------------- |
| **DM** | Demographics     | Subject ID, Age, Sex, Race    |
| **AE** | Adverse Events   | AE term, severity, onset date |
| **LB** | Laboratory Tests | Test name, result, units      |
| **VS** | Vital Signs      | Blood pressure, heart rate    |
| **EX** | Exposure         | Treatment dose, frequency     |

All datasets include **standardized variable naming conventions**, metadata, and controlled terminology (often linked to MedDRA or CDISC codelists).

### Example (Simplified SDTM AE Domain)

| STUDYID | USUBJID | AETERM   | AESEV | AESTDTC    |
| ------- | ------- | -------- | ----- | ---------- |
| STUDY01 | SUBJ001 | Headache | MILD  | 2024-06-15 |

## 3. ADaM (Analysis Data Model)

### Purpose

ADaM defines **analysis-ready datasets** derived from SDTM data. It ensures traceability between raw data and statistical results (e.g., tables, figures, and listings in clinical study reports).

### Structure

Common ADaM datasets include:

| Dataset  | Description                                                  |
| -------- | ------------------------------------------------------------ |
| **ADSL** | Subject-level analysis dataset (e.g., baseline demographics) |
| **ADAE** | Adverse events analysis dataset                              |
| **ADLB** | Laboratory results for analysis                              |
| **ADVS** | Vital signs for analysis                                     |

### Traceability

Each derived ADaM variable must link back to its SDTM origin through clear metadata documentation.

### Example

| USUBJID | PARAM       | AVISIT | AVAL | CHG |
| ------- | ----------- | ------ | ---- | --- |
| SUBJ001 | Systolic BP | Week 8 | 120  | -5  |

## 4. Relationship Between SDTM and ADaM

```
Raw CRF Data
    ↓  (Transformation)
SDTM (Standardized Study Data)
    ↓  (Derivation)
ADaM (Analysis-Ready Data)
    ↓
Statistical Outputs (Tables, Figures, Listings)
```

## 5. Controlled Terminology and Integration

CDISC models use controlled vocabularies maintained by the **NCI EVS (National Cancer Institute – Enterprise Vocabulary Services)**.

| Domain               | Linked Vocabulary           |
| -------------------- | --------------------------- |
| **Adverse Events**   | MedDRA                      |
| **Laboratory Tests** | LOINC                       |
| **Units**            | UCUM                        |
| **Drugs**            | WHO Drug Dictionary, RxNorm |

## 6. Regulatory Adoption

| Regulatory Body  | Requirement                                          |
| ---------------- | ---------------------------------------------------- |
| **FDA (U.S.)**   | Requires CDISC SDTM and ADaM formats for submissions |
| **PMDA (Japan)** | Mandates CDISC compliance for eCTD submissions       |
| **EMA (Europe)** | Accepts CDISC standards for harmonized submissions   |

## 7. Governance and Access

- **Maintained by:** Clinical Data Interchange Standards Consortium (CDISC)
- **Key standards:** SDTM, ADaM, SEND (for nonclinical studies), Define-XML
- **Access:** [https://www.cdisc.org](https://www.cdisc.org)
