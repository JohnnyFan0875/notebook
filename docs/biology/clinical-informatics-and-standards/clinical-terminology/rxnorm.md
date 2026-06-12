# RxNorm

## 1. Overview

**RxNorm** is a standardized nomenclature for **clinical drugs** maintained by the **U.S. National Library of Medicine (NLM)**. It provides normalized names, identifiers, and relationships among drug concepts to ensure semantic interoperability across healthcare systems, e-prescribing networks, and research databases.

RxNorm connects various drug vocabularies—such as First Databank, Micromedex, and the FDA’s Structured Product Labeling (SPL)—into a single, consistent coding framework.

## 2. Structure of RxNorm Concepts

RxNorm organizes drugs into a **hierarchical system** of interrelated entities, each represented by a unique **RxCUI (RxNorm Concept Unique Identifier)**.

| Concept Type                     | Example                          | Description                                                        |
| -------------------------------- | -------------------------------- | ------------------------------------------------------------------ |
| **IN (Ingredient)**              | Acetaminophen                    | The active chemical substance                                      |
| **PIN (Precise Ingredient)**     | Acetaminophen anhydrous          | A more specific ingredient variant                                 |
| **BN (Brand Name)**              | Tylenol                          | Manufacturer-specific brand name                                   |
| **SCD (Semantic Clinical Drug)** | Acetaminophen 500 mg Oral Tablet | A precise clinical formulation (ingredient + strength + dose form) |
| **SBD (Semantic Branded Drug)**  | Tylenol 500 mg Oral Tablet       | Branded version of a clinical drug                                 |
| **DF (Dose Form)**               | Oral Tablet                      | The physical form and route of administration                      |

**Example:**
`RxCUI 198440` → _Acetaminophen 500 MG Oral Tablet (Tylenol)_

## 3. Key Features

- Provides a **standardized drug vocabulary** for EHRs and pharmacy systems.
- Supports **e-prescribing and medication reconciliation**.
- Facilitates **drug–drug interaction** and **allergy checking**.
- Maps to other coding systems, including **NDC (National Drug Code)**, **SNOMED CT**, and **ATC**.

## 4. Integration in Clinical Systems

| Framework               | RxNorm Usage                                                       |
| ----------------------- | ------------------------------------------------------------------ |
| **HL7 FHIR**            | `Medication.code` or `MedicationRequest.medicationCodeableConcept` |
| **OMOP-CDM**            | Populates `drug_concept_id` field in the drug exposure table       |
| **EHR / e-Prescribing** | Ensures consistent naming and dosage interpretation                |
| **Drug Databases**      | Links branded and generic drugs through RxCUI relationships        |

## 5. Maintenance and Access

- **Maintained by:** U.S. National Library of Medicine (NLM)
- **Update frequency:** Weekly (Monday releases)
- **Access:** Free download or API via [https://rxnav.nlm.nih.gov](https://rxnav.nlm.nih.gov)
