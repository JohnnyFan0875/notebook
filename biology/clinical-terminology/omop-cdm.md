# OMOP-CDM

## 1. Overview

The Observational Medical Outcomes Partnership – Common Data Model (**OMOP-CDM**) is a standardized data structure developed by the **Observational Health Data Sciences and Informatics (OHDSI)** initiative. It enables consistent representation, integration, and analysis of observational healthcare data from multiple sources — such as EHRs, claims, registries, and biobanks.

OMOP-CDM supports large-scale, reproducible research by transforming heterogeneous clinical data into a **common schema with standardized vocabularies** (LOINC, SNOMED CT, RxNorm, etc.).

## 2. Core Principles

| Principle                     | Description                                                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Standardized schema**       | All participating databases follow the same table structure and field definitions.                                 |
| **Standardized vocabularies** | Clinical concepts are mapped to standard terminologies (SNOMED CT, RxNorm, LOINC, ICD).                            |
| **Provenance preservation**   | Source data and mappings are traceable through concept IDs and source values.                                      |
| **Reproducible analytics**    | Standardized structure allows OHDSI tools (e.g., ATLAS, Achilles, CohortDiagnostics) to run analyses across sites. |

## 3. Data Model Structure

OMOP-CDM organizes data into relational tables grouped by domain:

| Domain                   | Example Tables                                                                 | Description                                                                    |
| ------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Person-level data**    | `person`, `observation_period`                                                 | Demographics and observation windows                                           |
| **Clinical events**      | `condition_occurrence`, `procedure_occurrence`, `drug_exposure`, `observation` | Captures clinical diagnoses, procedures, prescriptions, and other observations |
| **Measurement and labs** | `measurement`                                                                  | Quantitative or qualitative results (e.g., lab values)                         |
| **Health economics**     | `cost`, `payer_plan_period`                                                    | Claims and reimbursement data                                                  |
| **Metadata**             | `concept`, `concept_relationship`, `vocabulary`                                | Stores controlled terminology and relationships                                |

## 4. Vocabulary System

OMOP maintains its own **Standardized Vocabularies**, integrating multiple sources:

- **Conditions** → SNOMED CT
- **Drugs** → RxNorm
- **Measurements** → LOINC
- **Procedures** → CPT, ICD-9/10-PCS
- **Units** → UCUM

Each record is identified by a **concept_id**, ensuring semantic interoperability.

## 5. Example Schema Flow

```
EHR Source Data (ICD-10, Local codes)
        ↓  ETL (Extract–Transform–Load)
OMOP-CDM Tables (standardized schema)
        ↓
OHDSI Analytics (ATLAS, ACHILLES, CohortDiagnostics)
```

## 6. Tools and Ecosystem

| Tool                  | Function                                                        |
| --------------------- | --------------------------------------------------------------- |
| **ATLAS**             | Web-based cohort design and analysis platform                   |
| **ACHILLES**          | Data quality and characterization tool                          |
| **CohortDiagnostics** | Evaluates reproducibility and consistency of cohort definitions |
| **PLP / PLE**         | Predictive and population-level effect estimation frameworks    |

## 7. Governance and Access

- **Maintained by:** OHDSI community
- **Specification:** [https://ohdsi.github.io/CommonDataModel](https://ohdsi.github.io/CommonDataModel)
- **License:** Open and freely available (Apache 2.0)
- **Latest version:** v5.4 (2024)
