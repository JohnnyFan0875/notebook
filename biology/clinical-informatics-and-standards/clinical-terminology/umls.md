# UMLS (Unified Medical Language System)

## 1. Overview

The **Unified Medical Language System (UMLS)** is an integrated biomedical terminology system developed by the **U.S. National Library of Medicine (NLM)**.
Its goal is to **link diverse medical vocabularies and standards**—such as LOINC, SNOMED CT, MeSH, RxNorm, and ICD—into a unified framework that supports semantic interoperability, data integration, and natural language processing (NLP) in healthcare and biomedical research.

## 2. Core Components

UMLS is composed of three major knowledge sources:

| Component                      | Description                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| **Metathesaurus**              | A massive database of biomedical and health-related concepts, synonyms, and relationships aggregated from 200+ vocabularies.   |
| **Semantic Network**           | Defines the high-level semantic types (e.g., _Disease or Syndrome_, _Pharmacologic Substance_) and relationships between them. |
| **SPECIALIST Lexicon & Tools** | Provides linguistic resources for NLP, including morphological and syntactic information on biomedical terms.                  |

## 3. The Metathesaurus

The **UMLS Metathesaurus** is the core component, containing over 3 million biomedical concepts. Each concept is assigned a **Concept Unique Identifier (CUI)** that links equivalent terms across different terminologies.

| Example                                                                           | Description                     |
| --------------------------------------------------------------------------------- | ------------------------------- |
| **CUI:** C0011849                                                                 | Concept for _Diabetes Mellitus_ |
| **Linked vocabularies:** SNOMED CT (`44054006`), ICD-10 (`E11`), MeSH (`D003920`) |                                 |

This crosswalk allows data coded in different systems to be aligned under one unified concept.

## 4. Semantic Network

The **Semantic Network** provides a conceptual backbone for the UMLS, defining the semantic relationships among biomedical entities.

| Example Relationship                         | Meaning |
| -------------------------------------------- | ------- |
| _Insulin_ → _treats_ → _Diabetes Mellitus_   |         |
| _Bacteria_ → _causes_ → _Infectious Disease_ |         |

These relationships enable advanced reasoning, data mining, and AI applications in medical informatics.

## 5. SPECIALIST Lexicon & NLP Tools

The **SPECIALIST Lexicon** contains morphological and syntactic data on biomedical terms, supporting:

- Text mining and named-entity recognition (NER)
- Clinical documentation analysis
- Concept extraction from free-text EHR notes

The **Lexical Tools API** helps map natural-language text to UMLS concepts.

## 6. Integration and Applications

| Application Area              | Example Usage                                       |
| ----------------------------- | --------------------------------------------------- |
| **Clinical data integration** | Map ICD, SNOMED CT, and LOINC codes to shared CUIs  |
| **NLP / text mining**         | Identify biomedical entities in clinical narratives |
| **Ontology alignment**        | Harmonize concepts across datasets and standards    |
| **FHIR Terminology Services** | Provide mappings for concept translation            |

## 7. Governance and Access

- **Maintained by:** U.S. National Library of Medicine (NLM)
- **Updates:** Twice per year (January and July)
- **Access:** [https://www.nlm.nih.gov/research/umls](https://www.nlm.nih.gov/research/umls)
  (UMLS license required for download and API use)
