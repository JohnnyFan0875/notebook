# FHIR

## 1. Overview

**HL7 FHIR** (Fast Healthcare Interoperability Resources) is a modern, web-based standard developed by **Health Level Seven International (HL7)** for exchanging healthcare information electronically.

FHIR combines the best features of previous HL7 versions (v2, v3, CDA) with modern API design principles, supporting **RESTful APIs**, **JSON/XML serialization**, and **extensibility** for both clinical and administrative data.

## 2. Core Principles

| Principle                         | Description                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Resource-based**                | All data are represented as modular, reusable resources (e.g., Patient, Observation, Medication). |
| **RESTful architecture**          | Supports standard HTTP operations (`GET`, `POST`, `PUT`, `DELETE`).                               |
| **Interoperability by design**    | Enables systems to share data consistently using global terminologies (LOINC, SNOMED CT, RxNorm). |
| **Extensibility**                 | Allows customization via extensions without breaking compatibility.                               |
| **Human and machine readability** | Data can be serialized in JSON, XML, or Turtle (RDF).                                             |

## 3. FHIR Resource Model

FHIR organizes healthcare data into more than **150 resource types**. Each resource has a consistent structure (metadata + content + links).

| Resource Type   | Example                                 | Description                    |
| --------------- | --------------------------------------- | ------------------------------ |
| **Patient**     | Demographics, identifiers, contact info | Core patient record            |
| **Observation** | Lab results, vital signs, measurements  | e.g., Glucose, Blood Pressure  |
| **Condition**   | Clinical diagnosis or finding           | e.g., Diabetes Mellitus        |
| **Medication**  | Drugs and substances                    | e.g., Metformin 500 mg tablet  |
| **Procedure**   | Surgical or diagnostic interventions    | e.g., MRI brain scan           |
| **Encounter**   | Patient visit or admission              | e.g., Hospital admission event |

**Example (FHIR JSON snippet):**

```json
{
  "resourceType": "Observation",
  "id": "glucose",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "2345-7",
        "display": "Glucose [Mass/volume] in Serum or Plasma"
      }
    ]
  },
  "valueQuantity": {
    "value": 95,
    "unit": "mg/dL",
    "system": "http://unitsofmeasure.org",
    "code": "mg/dL"
  },
  "subject": { "reference": "Patient/123" }
}
```

## 4. Interoperability and Terminology Bindings

FHIR integrates directly with standardized vocabularies:

| Vocabulary    | Role in FHIR                                                             |
| ------------- | ------------------------------------------------------------------------ |
| **LOINC**     | Laboratory test identifiers (`Observation.code`)                         |
| **SNOMED CT** | Diagnoses, findings, and procedures (`Condition.code`, `Procedure.code`) |
| **RxNorm**    | Medications and drug products (`Medication.code`)                        |
| **UCUM**      | Units of measure (`Observation.valueQuantity.unit`)                      |

## 5. Implementation Layers

| Layer                     | Example                          | Purpose                                            |
| ------------------------- | -------------------------------- | -------------------------------------------------- |
| **RESTful API**           | `/Patient/123`                   | CRUD operations for resources                      |
| **Profiles & Extensions** | US Core, IPS                     | Customize base resources for national/regional use |
| **Terminology Services**  | Concept lookup, code translation | Bind FHIR elements to vocabularies                 |
| **Security**              | OAuth 2.0, SMART on FHIR         | Authentication and authorization framework         |

## 6. FHIR Versions and Profiles

- **Major releases:** DSTU2 → STU3 → R4 → R5 (current, 2024)
- **Profiles:** Constrain and extend base FHIR resources for local contexts (e.g., **US Core**, **International Patient Summary (IPS)**)
- **Implementation Guides (IGs):** Official specifications for specific workflows (e.g., immunization, oncology, genomics)

## 7. Relationship to Other Standards

| Standard                          | Integration with FHIR                                            |
| --------------------------------- | ---------------------------------------------------------------- |
| **openEHR**                       | Archetypes can be mapped to FHIR resources                       |
| **OMOP-CDM**                      | FHIR data can be ETL-transformed into analytical OMOP structures |
| **ICD / SNOMED / LOINC / RxNorm** | Used for semantic consistency in resource coding                 |
| **DICOM**                         | Imaging metadata linked via `ImagingStudy` resources             |

## 8. Governance and Access

- **Maintained by:** HL7 International
- **Open standard:** Freely available with community-driven updates
- **Official site:** [https://hl7.org/fhir](https://hl7.org/fhir)
- **Current release:** FHIR R5 (2024)
