# CPT / HCPCS

## 1. Overview

**CPT** (Current Procedural Terminology) and **HCPCS** (Healthcare Common Procedure Coding System) are two standardized systems used primarily in the **United States** for coding **medical procedures, services, and supplies**. They support administrative, billing, and insurance reimbursement processes, ensuring that medical procedures are recorded and interpreted consistently across healthcare institutions.

## 2. CPT (Current Procedural Terminology)

### Description

Developed and maintained by the **American Medical Association (AMA)**, CPT provides a uniform language for describing **medical, surgical, and diagnostic services** performed by healthcare professionals.

### Structure of CPT Codes

- CPT codes are **five-digit numeric codes**, sometimes followed by modifiers.
- Organized into three main categories:

| Category         | Purpose                                           | Example                                                |
| ---------------- | ------------------------------------------------- | ------------------------------------------------------ |
| **Category I**   | Standard medical procedures and services          | `99213` – Office/outpatient visit, established patient |
| **Category II**  | Performance measurement / quality reporting       | `0001F` – Tobacco use screening performed              |
| **Category III** | Emerging technologies and experimental procedures | `0075T` – Computer-aided detection for MRI             |

### Common Use Cases

- Insurance billing and reimbursement
- Hospital and outpatient documentation
- Performance reporting and quality metrics

## 3. HCPCS (Healthcare Common Procedure Coding System)

### Description

HCPCS is a two-level system developed by the **Centers for Medicare & Medicaid Services (CMS)** to complement CPT and cover additional services and items not included in CPT.

### Structure of HCPCS Codes

| Level        | Description                                                                                   | Example                                         |
| ------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Level I**  | CPT codes maintained by AMA                                                                   | `99213` – Office visit                          |
| **Level II** | Alphanumeric codes for supplies, durable medical equipment, drugs, and non-physician services | `A0429` – Ambulance service, basic life support |

### Common Use Cases

- Medicare/Medicaid billing
- Durable medical equipment (DME) tracking
- Drugs and biologics reimbursement (e.g., injectables)

## 4. Integration and Mapping

| Framework              | Role of CPT/HCPCS                                                      |
| ---------------------- | ---------------------------------------------------------------------- |
| **FHIR**               | Used in `Procedure.code`, `ServiceRequest.code`, and billing resources |
| **OMOP-CDM**           | Stored in the `procedure_occurrence` table as `procedure_concept_id`   |
| **Claims databases**   | Core identifiers for billing and cost analyses                         |
| **SNOMED CT / ICD-10** | Crosswalk available for clinical-to-billing code translation           |

## 5. Maintenance and Access

| System    | Maintained by                                  | Update Frequency | Access                                               |
| --------- | ---------------------------------------------- | ---------------- | ---------------------------------------------------- |
| **CPT**   | American Medical Association (AMA)             | Annual (October) | [https://www.ama-assn.org](https://www.ama-assn.org) |
| **HCPCS** | Centers for Medicare & Medicaid Services (CMS) | Quarterly        | [https://www.cms.gov](https://www.cms.gov)           |
