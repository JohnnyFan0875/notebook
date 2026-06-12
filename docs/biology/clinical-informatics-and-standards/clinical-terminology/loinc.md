# LOINC

## 1. Overview

**LOINC** (Logical Observation Identifiers Names and Codes) is a global standard for identifying laboratory and clinical observations. Developed by the **Regenstrief Institute** and maintained in collaboration with the **U.S. National Library of Medicine (NLM)**, LOINC enables consistent exchange and aggregation of clinical results across systems and institutions.

LOINC provides a **universal code system** for tests, measurements, and observations, allowing healthcare data to be shared unambiguously across different laboratories and EHR systems.

## 2. Structure of a LOINC Term

Each LOINC entry describes a single, testable observation defined by **six core attributes**:

| Attribute     | Description                                                | Example                      |
| ------------- | ---------------------------------------------------------- | ---------------------------- |
| **Component** | What is being measured, evaluated, or observed             | _Glucose_                    |
| **Property**  | The characteristic or attribute measured                   | _MCnc_ (Mass concentration)  |
| **Time**      | The interval of time over which an observation is made     | _Pt_ (Point in time)         |
| **System**    | The sample or system on which the measurement is performed | _Ser/Plas_ (Serum or plasma) |
| **Scale**     | The scale of measurement                                   | _Qn_ (Quantitative)          |
| **Method**    | The method used to make the measurement (optional)         | _Enzymatic_                  |

**Example:**
LOINC code **2345-7** corresponds to:
**Glucose [Mass/volume] in Serum or Plasma – Point in time – Quantitative – Enzymatic method**

## 3. Categories of Use

LOINC codes are widely applied across healthcare:

- **Laboratory tests:** Blood chemistry, hematology, microbiology, molecular diagnostics
- **Clinical measurements:** Vital signs, height, weight, BMI
- **Clinical documents:** Discharge summaries, radiology reports, pathology findings
- **Survey instruments:** Patient questionnaires such as PHQ-9, PROMIS

## 4. LOINC in Interoperability

LOINC is an integral component of modern interoperability frameworks:

| Framework                   | Role of LOINC                                                            |
| --------------------------- | ------------------------------------------------------------------------ |
| **HL7 FHIR**                | Used in `Observation.code`, `DiagnosticReport.code` fields               |
| **OMOP-CDM**                | Maps to measurement and observation tables                               |
| **Public health reporting** | Enables standardized reporting of laboratory results to national systems |

## 5. Maintenance and Access

- **Maintained by:** Regenstrief Institute & NLM
- **Update frequency:** Twice yearly (June and December)
- **Access:** Free download from [https://loinc.org](https://loinc.org)
