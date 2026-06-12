# MedDRA

## 1. Overview

**MedDRA** (Medical Dictionary for Regulatory Activities) is a standardized, multilingual terminology used for coding and classifying **medical information related to drugs, biologics, and medical devices**, particularly in clinical trials and post-marketing safety reporting.

It is maintained by the **International Council for Harmonisation (ICH)** and is globally recognized by regulatory agencies such as the **FDA**, **EMA**, and **PMDA**.
MedDRA enables consistent communication of **adverse events (AEs)**, **indications**, and **medical histories** across organizations and jurisdictions.

## 2. Purpose

MedDRA provides a **hierarchical structure** that allows medical conditions to be recorded at varying levels of detail while maintaining consistency in classification.
It supports:

- Adverse event coding in **clinical trials** and **pharmacovigilance**.
- Regulatory submissions and safety reports (e.g., **E2B** format).
- Signal detection and risk management.

## 3. Hierarchical Structure

MedDRA is a **five-level hierarchy**, from the broadest to the most specific term:

| Level                            | Description                                 | Example                             |
| -------------------------------- | ------------------------------------------- | ----------------------------------- |
| **System Organ Class (SOC)**     | Broadest level, groups by organ or etiology | _Cardiac disorders_                 |
| **High Level Group Term (HLGT)** | Groups related HLTs                         | _Heart failures_                    |
| **High Level Term (HLT)**        | Groups related PTs                          | _Cardiac failure and complications_ |
| **Preferred Term (PT)**          | Single medical concept used for coding      | _Congestive heart failure_          |
| **Lowest Level Term (LLT)**      | Synonyms or lexical variants of PT          | _CHF_, _Heart failure NOS_          |

## 4. Coding Example

```
Adverse Event Reported: "Heart failure, acute on chronic"
 → LLT: Heart failure acute on chronic
 → PT: Congestive heart failure
 → HLT: Cardiac failure and complications
 → HLGT: Heart failures
 → SOC: Cardiac disorders
```

This hierarchical mapping ensures consistent aggregation of related events in safety analyses.

## 5. Integration with Other Standards

| Standard                         | Integration with MedDRA                                                 |
| -------------------------------- | ----------------------------------------------------------------------- |
| **CDISC SDTM**                   | Used in AE (Adverse Events) domain via AETERM / AEDECOD variables       |
| **E2B / ICH Guidelines**         | Required for electronic adverse event reporting                         |
| **WHO Drug Dictionary / RxNorm** | Can be cross-referenced for drug–event relationships                    |
| **SNOMED CT**                    | Partial mappings exist for interoperability with clinical terminologies |

## 6. Maintenance and Updates

- **Maintained by:** ICH MedDRA Maintenance and Support Services Organization (MSSO)
- **Release frequency:** Twice per year (March and September)
- **Languages:** Available in 11 languages (English, Japanese, Chinese, Spanish, etc.)
- **Versioning:** Each release includes a version number (e.g., v27.0)

## 7. Use in Regulatory Submissions

| Agency           | Implementation                                        |
| ---------------- | ----------------------------------------------------- |
| **FDA (U.S.)**   | Mandatory for electronic AE submissions (e.g., FAERS) |
| **EMA (Europe)** | Required for EudraVigilance reporting                 |
| **PMDA (Japan)** | Required for post-marketing safety data               |

## 8. Access and Licensing

- **Website:** [https://www.meddra.org](https://www.meddra.org)
- **Access:** Free for non-commercial use (academic, regulatory, or government institutions)
- **Commercial license:** Required for industry use
