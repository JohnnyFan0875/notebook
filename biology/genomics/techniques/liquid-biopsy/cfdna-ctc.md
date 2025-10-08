# CTC and cfDNA in Liquid Biopsy

## 1. Fundamental Definitions and Differences

| Feature                    | CTC (Circulating Tumor Cells)                                                | cfDNA (Cell-Free DNA) / ctDNA (Circulating Tumor DNA)                            |
| -------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Origin**                 | Intact tumor cells shed from solid tumors into the bloodstream               | DNA fragments released by tumor cell apoptosis, necrosis, or active secretion    |
| **Composition**            | Complete cells containing nuclei, RNA, and proteins                          | Short DNA fragments (typically 150–200 bp)                                       |
| **Concentration in Blood** | Very low (1–10 cells per mL)                                                 | Relatively higher (ng/mL range)                                                  |
| **Analytical Level**       | Cellular level: morphology, single-cell RNA/DNA sequencing, drug testing     | Molecular level: mutation, methylation, CNV analysis                             |
| **Clinical Utility**       | Tumor metastasis research, drug resistance monitoring, single-cell profiling | Mutation detection, treatment response, minimal residual disease (MRD) detection |

## 2. Biological Relationship Between CTC and cfDNA

**Shared origin:** Both originate from tumor cells entering the bloodstream. When CTCs die or are cleared by the immune system, they release cfDNA—thus, part of cfDNA derives from dead or necrotic CTCs.

**Complementary tumor indicators:**

- **CTC:** Represents _viable tumor cells_, reflecting invasive and metastatic potential.
- **cfDNA:** Represents _cellular debris_, reflecting tumor burden and cell turnover.

Combining both enables simultaneous monitoring of tumor activity (via CTCs) and cell death dynamics (via cfDNA).

**Molecular concordance and heterogeneity:**

- CTCs and cfDNA often share driver mutations (e.g., _EGFR, KRAS, TP53_), but discrepancies occur due to tumor heterogeneity.
- cfDNA can capture broader mutational landscapes, whereas CTCs confirm which mutations exist in _metastasis-capable live cells_.

## 3. Complementary Clinical Applications

| Clinical Context                      | Role of CTC                                                                          | Role of cfDNA                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| **Cancer diagnosis**                  | Provides morphological and immunophenotypic information; helps identify tumor origin | Rapid mutation detection; supports early detection         |
| **Prognosis & metastasis monitoring** | CTC count and EMT markers correlate with metastatic risk                             | cfDNA quantity and mutation frequency reflect tumor burden |
| **Treatment response**                | Enables single-cell resistance mechanism and protein expression profiling            | Detects resistance mutations (e.g., _EGFR T790M_)          |
| **MRD detection**                     | Lower sensitivity but high specificity                                               | High sensitivity; detects very low-frequency mutations     |

## 4. Comparison of Cancer Types Suitable for Detection

| Cancer Type                      | CTC Characteristics                                                           | cfDNA Characteristics                                                 | Remarks                            |
| -------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------- |
| **Breast cancer**                | High detection rate (FDA-approved CellSearch system); strong prognostic value | Detects _PIK3CA_, _ESR1_ mutations; used for therapy monitoring       | Both well-established applications |
| **Prostate cancer**              | Reflects metastasis and androgen receptor variants (AR-V7)                    | Detects _BRCA1/2_, _ATM_ mutations                                    | Combined use in mCRPC common       |
| **Lung cancer**                  | CTC counts low but suitable for single-cell analysis                          | High sensitivity; detects _EGFR, KRAS, ALK_ mutations                 | cfDNA is clinical mainstream       |
| **Colorectal cancer**            | Reflects metastasis and recurrence risk                                       | Detects _KRAS_, _NRAS_, _BRAF_ mutations; predicts anti-EGFR response | cfDNA more sensitive               |
| **Liver cancer**                 | Early detection and metastasis monitoring possible                            | Methylation or _TP53_ mutations indicate early-stage disease          | cfDNA rapidly developing           |
| **Pancreatic / Biliary cancers** | Difficult to detect CTCs (low vascular permeability)                          | High cfDNA sensitivity; detects _KRAS_ mutations                      | cfDNA preferred                    |
| **Brain tumors (Glioma)**        | Rare due to blood–brain barrier                                               | Low in plasma but detectable in CSF cfDNA                             | CSF cfDNA more reliable            |
| **Gastric / Esophageal cancer**  | CTCs indicate metastatic progression                                          | cfDNA detects _HER2_, _TP53_, methylation markers                     | Both promising                     |

## 5. Sensitivity and Applicability Summary

| Aspect                       | CTC                                             | cfDNA                                               |
| ---------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Biological Material**      | Viable cells                                    | DNA fragments                                       |
| **Technical Difficulty**     | High (complex isolation)                        | Moderate (simple plasma extraction)                 |
| **Sensitivity**              | Moderate (rare cells)                           | High (abundant DNA)                                 |
| **Specificity**              | High; confirms tumor origin                     | Moderate; may include non-tumor cfDNA               |
| **Best-suited Cancer Types** | Metastatic solid tumors (esp. breast, prostate) | Broadly applicable (esp. lung)                      |
| **Clinical Use Today**       | Prognosis & metastasis monitoring               | Mutation detection, therapy & recurrence monitoring |

## 6. Comparative Application for Metastasis Detection

| Aspect                 | CTC                                                                          | cfDNA                                                              |
| ---------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Core Role**          | Represents viable metastatic cells with adhesion and colonization capability | Represents DNA from dead tumor cells, lacking metastatic potential |
| **Biological Meaning** | Indicates invasion, EMT, and stemness                                        | Reflects tumor burden and turnover rate                            |
| **Main Purposes**      | - Study metastatic mechanisms                                                |                                                                    |

- Track metastasis risk and site
- Analyze EMT and stemness markers | - Detect mutations & methylation
- Monitor treatment and recurrence
- Identify drug-resistance mutations (_EGFR T790M_) |
  | **Technical Challenges** | Rare, hard to isolate, less standardized | Easier to process, high sensitivity |

### ➜ **Therefore:**

- For studying or detecting **tumor metastasis mechanisms**, **CTC** is preferred because it represents _live, metastasis-capable cells_.
- **cfDNA**, while not indicating live cell migration, provides a _molecular snapshot_ of tumor activity and treatment response.

## 7. Main Clinical Applications of cfDNA / ctDNA

1. **Mutation Detection and Targeted Therapy Guidance**

   - Detects driver mutations (_EGFR, KRAS, BRAF, PIK3CA_).
   - Enables noninvasive genotyping when tissue samples are unavailable.
   - Example: _EGFR_ mutation testing in lung cancer to determine TKI eligibility.

2. **Therapeutic Monitoring and Recurrence Tracking**

   - cfDNA levels correlate with tumor burden.
   - Drop after therapy = good response; rise = recurrence or resistance.
   - Detectable changes precede radiologic evidence.

3. **Minimal Residual Disease (MRD) Detection**

   - Detecting ctDNA post-treatment indicates microscopic residual disease.
   - More sensitive than imaging or conventional biomarkers (e.g., CEA, CA‑125).

4. **Early Cancer Screening (MCED)**

   - Multi-cancer early detection via methylation or fragmentation profiles.
   - Example: GRAIL's _Galleri_ test screens for >50 cancer types.

## 8. Strategic Recommendations by Research / Clinical Goal

| Objective                                          | Preferred Choice         | Rationale                                                            |
| -------------------------------------------------- | ------------------------ | -------------------------------------------------------------------- |
| Metastatic mechanism / EMT / stemness research     | **CTC**                  | Provides live cells for morphology, RNA, and functional analysis     |
| Metastasis risk or recurrence prediction           | **CTC + cfDNA combined** | Complementary: CTC shows activity, cfDNA shows burden                |
| Targeted therapy mutation detection (_EGFR, KRAS_) | **cfDNA**                | High sensitivity, noninvasive, standardized clinically               |
| Treatment monitoring / MRD detection               | **cfDNA**                | Quantitative and sensitive for long-term tracking                    |
| Early cancer screening                             | **cfDNA**                | Methylation and fragmentation profiles enable multi-cancer detection |

## 9. Summary

- **CTC**: Represents _live, metastasis-competent tumor cells_ — ideal for studying invasion, metastasis, and cellular-level behavior.
- **cfDNA**: Represents _molecular fragments of tumor genomes_ — ideal for genetic profiling, therapy monitoring, and recurrence detection.
- **Integration of CTC and cfDNA** provides a comprehensive, dual-layer view (cellular + molecular) of tumor dynamics, forming the foundation of modern **precision oncology**.
