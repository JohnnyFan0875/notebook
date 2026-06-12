# openEHR

## 1. Overview

**openEHR** is an open, standards-based framework for designing, storing, and exchanging **electronic health records (EHRs)**.
It focuses on **semantic interoperability**, ensuring that clinical data can be shared, interpreted, and reused across different systems, institutions, and countries.

Unlike message-based standards (e.g., HL7 v2, FHIR), openEHR defines how clinical information is **modeled and persisted** in databases using a robust two-level modeling architecture.

## 2. Key Concepts

| Concept                  | Description                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Two-level modeling**   | Separates the technical data structure (Reference Model) from the clinical content definitions (Archetypes and Templates).           |
| **Archetype**            | A reusable, machine-readable model that defines the structure and semantics of a clinical concept (e.g., blood pressure, diagnosis). |
| **Template**             | Combines multiple archetypes to create a use-case-specific structure (e.g., discharge summary, encounter note).                      |
| **Reference Model (RM)** | Defines the fundamental building blocks (e.g., data types, composition, observations).                                               |
| **EHR Persistence**      | openEHR defines how structured data is stored for long-term semantic stability.                                                      |

## 3. openEHR Architecture

```
+--------------------------------------------------+
|   Applications (UI, EHR systems, analytics)      |
+--------------------------------------------------+
|   Templates (composed of archetypes)             |
+--------------------------------------------------+
|   Archetypes (clinical concept definitions)       |
+--------------------------------------------------+
|   Reference Model (core data structures)          |
+--------------------------------------------------+
|   Data persistence / versioning / audit trail     |
+--------------------------------------------------+
```

This design allows openEHR systems to evolve clinically (by updating archetypes) without changing underlying database schemas.

## 4. Archetypes and Templates

### Archetype Example – Blood Pressure

```
openEHR-EHR-OBSERVATION.blood_pressure.v1
 ├── systolic: Quantity (mmHg)
 ├── diastolic: Quantity (mmHg)
 ├── position: Coded text
 ├── time: DateTime
```

### Template Example – Vital Signs

Combines multiple archetypes:

- Blood Pressure
- Heart Rate
- Body Temperature

## 5. Interoperability

| Standard            | Relationship with openEHR                                                            |
| ------------------- | ------------------------------------------------------------------------------------ |
| **HL7 FHIR**        | openEHR can export or map archetypes to FHIR resources (e.g., Observation, Patient). |
| **LOINC**           | Used within archetypes for lab test identifiers.                                     |
| **SNOMED CT / ICD** | Integrated for coded value sets and clinical terminology bindings.                   |
| **OMOP-CDM**        | Can be used as a downstream analytical model for harmonized data export.             |

## 6. Governance and Tools

| Component            | Description                                                                          |
| -------------------- | ------------------------------------------------------------------------------------ |
| **Maintained by**    | openEHR International Foundation                                                     |
| **Modeling tools**   | Archetype Designer, Template Designer, Archetype Editor                              |
| **Programming APIs** | Available in Java, .NET, Python, and REST APIs                                       |
| **Repositories**     | Clinical Knowledge Manager (CKM): [https://ckm.openehr.org](https://ckm.openehr.org) |

## 7. Advantages

- Long-term semantic stability
- Clinician-driven data modeling
- Fully open specification and governance
- Support for multilingual, multi-domain health records
- Compatible with FHIR, SNOMED CT, and LOINC
