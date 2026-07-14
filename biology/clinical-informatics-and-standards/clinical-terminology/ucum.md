# UCUM

## 1. Overview

The **Unified Code for Units of Measure (UCUM)** is a standardized system designed to ensure the **consistent representation of measurement units** across electronic health records (EHRs), laboratory systems, and medical data exchanges.

Developed by **Regenstrief Institute** (the same organization behind LOINC), UCUM provides a computer-readable format for expressing all physical measurement units used in healthcare, science, and engineering.

## 2. Purpose

In clinical and laboratory data, units such as `mg/dL`, `mmol/L`, or `µg/m³` are essential for interpreting quantitative results. However, variations in notation (e.g., `mg/dl` vs. `mg/dL`) can cause data incompatibility.
UCUM solves this problem by defining a **formal syntax** and **canonical representation** for all units.

## 3. Key Features

| Feature                      | Description                                                         |
| ---------------------------- | ------------------------------------------------------------------- |
| **Comprehensive coverage**   | Includes SI, ISO, and non-SI units (e.g., mg, mL, IU)               |
| **Machine-readable**         | Designed for automated data validation and exchange                 |
| **Compatible with LOINC**    | Used in laboratory result units (e.g., glucose [Mass/volume] mg/dL) |
| **Case-sensitive syntax**    | Differentiates between `m` (meter) and `M` (molar)                  |
| **Dimensionally consistent** | Each derived unit can be expressed in base units                    |

## 4. Syntax Examples

| Expression | Meaning                                    |
| ---------- | ------------------------------------------ |
| `mg/dL`    | milligram per deciliter                    |
| `mmol/L`   | millimole per liter                        |
| `kg.m/s2`  | kilogram meter per second squared (Newton) |
| `10*3/uL`  | thousand per microliter                    |
| `Cel`      | degree Celsius                             |

## 5. Integration in Health IT Standards

| Framework    | UCUM Role                                                                        |
| ------------ | -------------------------------------------------------------------------------- |
| **LOINC**    | Defines the units of measurement for quantitative lab tests                      |
| **FHIR**     | Standard unit representation in `Quantity.value` and `Observation.valueQuantity` |
| **OMOP-CDM** | Harmonizes unit data in the `measurement` table                                  |
| **DICOM**    | Supports consistent unit display for imaging-related measurements                |

## 6. Governance and Access

- **Maintained by:** Regenstrief Institute
- **Current release:** UCUM 1.9 (Ongoing updates)
- **Access and documentation:** [https://unitsofmeasure.org](https://unitsofmeasure.org)
