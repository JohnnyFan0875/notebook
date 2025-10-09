# ICD

## 1. Overview

The **International Classification of Diseases (ICD)** is a global standard for coding diseases, signs, symptoms, abnormal findings, and external causes of injury. It is maintained by the **World Health Organization (WHO)** and serves as the primary classification system for **morbidity and mortality statistics**, **health insurance claims**, and **public health reporting**.

ICD is widely used for clinical documentation, billing, and epidemiological research. The most current versions are **ICD-10** (1990) and **ICD-11** (released in 2019).

## 2. ICD-10 Overview

ICD-10 organizes diseases into **chapters**, each representing a body system or disease category. Codes are alphanumeric and generally consist of **one letter followed by two digits** (e.g., `E11`).

| Example   | Description                                        |
| --------- | -------------------------------------------------- |
| **E11**   | Type 2 diabetes mellitus                           |
| **I10**   | Essential (primary) hypertension                   |
| **C34.1** | Malignant neoplasm of upper lobe, bronchus or lung |

### Structure:

```
E11 — Type 2 diabetes mellitus
 ├── E11.0 — With coma
 ├── E11.3 — With ophthalmic complications
 ├── E11.9 — Without complications
```

## 3. ICD-11 Overview

ICD-11 represents a major digital transformation of the ICD framework. It is:

- **Ontology-based** (built with semantic relationships)
- **Machine-readable and API-accessible**
- **Cross-linked with SNOMED CT, LOINC, and other modern terminologies**

### ICD-11 Code Structure

ICD-11 codes are alphanumeric, with up to **seven characters** and a new hierarchical model.

| Example  | Description                                   |
| -------- | --------------------------------------------- |
| **5A11** | Type 2 diabetes mellitus                      |
| **1A00** | Cholera due to _Vibrio cholerae_ O1 serogroup |

### Advantages over ICD-10

- Improved digital data handling and web API access
- More detailed clinical granularity
- Enhanced interoperability with modern EHR systems

## 4. Integration and Mapping

| Framework            | Usage                                                                        |
| -------------------- | ---------------------------------------------------------------------------- |
| **ICD-10-CM (U.S.)** | Clinical modification for diagnosis coding in hospitals and insurance claims |
| **ICD-10-PCS**       | Procedure coding system for inpatient procedures (U.S.)                      |
| **SNOMED CT**        | Mapped for detailed semantic representation                                  |
| **FHIR / OMOP-CDM**  | ICD codes mapped to standardized vocabularies for interoperability           |

## 5. Governance and Access

- **Maintained by:** World Health Organization (WHO)
- **Releases:** ICD-10 (1990), ICD-11 (2019)
- **Access:** [https://icd.who.int](https://icd.who.int)
