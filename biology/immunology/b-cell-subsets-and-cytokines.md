# B Cell Subsets and Cytokines

## 1. Major B Cell Types and Their Functions

| Subset                            | Location / Phenotype                        | Main Function                                                            | Typical Markers       |
| --------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------ | --------------------- |
| **Naïve B cell**                  | Peripheral blood, secondary lymphoid organs | Antigen recognition via BCR (IgM, IgD)                                   | CD19⁺ CD20⁺ IgM⁺ IgD⁺ |
| **Activated B cell**              | Secondary lymphoid follicles                | Undergoes clonal expansion and class-switch recombination (CSR)          | CD69⁺ CD86⁺           |
| **Germinal Center (GC) B cell**   | Germinal centers of lymph nodes and spleen  | Somatic hypermutation (SHM) and affinity maturation                      | BCL6⁺ AID⁺            |
| **Memory B cell**                 | Circulation and lymphoid tissues            | Long-term antigen memory; rapid reactivation                             | CD27⁺ CD38⁻           |
| **Plasma cell**                   | Bone marrow, mucosa                         | Secretes antibodies (IgG, IgA, etc.)                                     | CD138⁺ Blimp-1⁺       |
| **Regulatory B cell (Breg)**      | Peripheral blood, spleen                    | Secretes IL-10, TGF-β; suppresses excessive inflammation                 | CD19⁺ CD24hi CD38hi   |
| **Marginal Zone (MZ) B cell**     | Spleen marginal zone                        | Rapid antibody response to T-independent antigens (LPS, polysaccharides) | IgMhi CD21hi CD1d⁺    |
| **Follicular B cell (FO B cell)** | Lymph node follicles                        | T-dependent antibody responses                                           | CD23⁺ IgD⁺            |

## 2. Cytokines Regulating B Cells

調控 B 細胞的細胞激素（IL-4、IL-6、IL-21、BAFF、APRIL…）見 [細胞激素網路](cytokines.md)。

## 3. B Cell Activation Pathways

| Activation Type            | Antigen Type               | Requirement                           | Example Antigens                    | Major Outcome                                          |
| -------------------------- | -------------------------- | ------------------------------------- | ----------------------------------- | ------------------------------------------------------ |
| **T-dependent activation** | Protein antigens           | Requires Tfh help (CD40–CD40L, IL-21) | Tetanus toxoid, viral proteins      | Isotype switching, affinity maturation, memory B cells |
| **T-independent type I**   | Polymeric antigens (LPS)   | Direct activation via TLRs            | Bacterial LPS                       | IgM response, no memory                                |
| **T-independent type II**  | Repetitive polysaccharides | Crosslinking of BCR                   | Pneumococcal capsule polysaccharide | IgM response, minimal memory                           |

## 4. Class-Switch Recombination

類別轉換與誘導的細胞激素（含人類與小鼠的差異）見 [細胞激素網路：抗體類別轉換](cytokines.md#抗體類別轉換-class-switching)。

## 5. Functional Relationship Between T and B Cells

```
Tfh (IL-21, CD40L)
        ↓
B cell activation → Germinal center formation
        ↓
    Somatic hypermutation (AID)
        ↓
  Class-switch recombination → Memory B / Plasma cell
```

**Key checkpoints:**

- **CD40–CD40L interaction**: essential for T-dependent activation
- **BCL6–Blimp-1 balance**: determines GC vs plasma cell fate
- **IL-21**: master cytokine driving antibody affinity maturation

## 6. Regulatory and Pathological Contexts

| Immune Context                          | Key B Cell Type / Cytokine                  | Function / Outcome               |
| --------------------------------------- | ------------------------------------------- | -------------------------------- |
| **Autoimmune diseases (e.g., SLE, RA)** | Overactive GC B cells; excessive IL-6, BAFF | Autoantibody production          |
| **Allergic diseases**                   | TH2 → IL-4 / IL-13 → IgE B cells            | Type I hypersensitivity          |
| **Mucosal immunity (gut, lung)**        | IgA⁺ plasma cells; TGF-β, IL-5              | Barrier protection               |
| **Chronic infection**                   | Tfh–B cell overactivation; IL-21            | Persistent GC reaction           |
| **Cancer (multiple myeloma)**           | Malignant plasma cells; IL-6 dependency     | Excessive monoclonal antibodies  |
| **Immunoregulation**                    | Breg via IL-10, TGF-β                       | Suppresses TH1/TH17 inflammation |

## Summary

- **B cells** progress through distinct stages — naive → activated → germinal center → plasma or memory cells — under cytokine and T cell regulation.
- **Key cytokines:** IL-4, IL-6, IL-10, IL-21, BAFF, TGF-β, IFN-γ.
- **Tfh** cells are central regulators, coordinating B cell differentiation via **CD40L and IL-21**.
- B cells are not only **antibody producers**, but also play regulatory and antigen-presenting roles in immune homeostasis and pathology.
