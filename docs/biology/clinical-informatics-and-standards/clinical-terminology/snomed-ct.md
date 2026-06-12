# SNOMED CT

## 1. Overview

**SNOMED CT** (Systematized Nomenclature of Medicine – Clinical Terms) is the world’s most comprehensive, multilingual clinical healthcare terminology. It is maintained by **SNOMED International** and provides standardized codes for diseases, clinical findings, procedures, body structures, organisms, and other healthcare concepts.

SNOMED CT serves as the foundation for semantic interoperability, enabling clinical information to be consistently represented and shared across electronic health record (EHR) systems, research databases, and healthcare analytics platforms.

## 2. Concept Model

SNOMED CT is built on an **ontology-based model**. Each medical concept has a unique identifier and is connected to other concepts through defined relationships.

| Element                 | Description                                                                  | Example                                                  |
| ----------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Concept ID**          | Unique numeric identifier for each concept                                   | `44054006`                                               |
| **Preferred Term (PT)** | The most common name used for a concept                                      | _Type 2 diabetes mellitus_                               |
| **Synonyms**            | Alternate or local names for the same concept                                | _Adult-onset diabetes_, _Non-insulin-dependent diabetes_ |
| **Relationships**       | Logical links that define clinical meaning (e.g., "is a", "associated with") | _Type 2 diabetes mellitus → is a → Diabetes mellitus_    |

## 3. Hierarchical Structure

SNOMED CT concepts are organized hierarchically, from general to specific.
Example:

```
Clinical finding
 └── Endocrine disorder
      └── Diabetes mellitus
           └── Type 2 diabetes mellitus
```

This hierarchical design enables inheritance of properties, consistent classification, and semantic querying.

## 4. Domains Covered

| Domain                           | Example Concepts                     |
| -------------------------------- | ------------------------------------ |
| **Clinical findings / diseases** | Pneumonia, Asthma, Diabetes mellitus |
| **Procedures**                   | Appendectomy, MRI scan of brain      |
| **Body structures**              | Heart, Liver, Left lung              |
| **Organisms / substances**       | Escherichia coli, Insulin            |
| **Observable entities**          | Blood pressure, Heart rate           |
| **Pharmaceutical products**      | Metformin, Insulin glargine          |

## 5. Integration and Interoperability

| Framework                   | Usage                                                                     |
| --------------------------- | ------------------------------------------------------------------------- |
| **HL7 FHIR**                | `Condition.code`, `Procedure.code`, and other clinical elements           |
| **OMOP-CDM**                | Maps to `condition_concept_id`, `procedure_concept_id`, `drug_concept_id` |
| **ICD-10 / ICD-11 Mapping** | Enables crosswalk between billing and clinical ontologies                 |
| **EHR Systems**             | Standardized diagnosis, procedure, and problem lists                      |

## 6. Maintenance and Access

- **Maintained by:** SNOMED International (formerly IHTSDO)
- **Release frequency:** Twice per year (January and July)
- **License:** Free for member countries (including most OECD nations)
- **Access:** [https://www.snomed.org](https://www.snomed.org)
