# Types of Censoring in Survival Analysis

Censoring occurs when the exact survival time of a subject is **not fully observed**.  
Instead of knowing the exact time of the event (e.g., death, relapse), we only know partial information.  
Handling censoring correctly is fundamental in survival analysis.

## 1. Right Censoring (Most Common)

- The **event has not occurred** by the end of study or last follow-up.
- We only know the subject survived at least up to the censoring time.

**Examples:**

- Patient still alive at study end.
- Patient withdraws from the study.
- Patient lost to follow-up.

**Notation:**

- Observed time = $T_i = \min(\text{event time}, \text{censoring time})$
- Indicator variable $ \delta_i = 1 $ if event observed, 0 if censored.

## 2. Left Censoring

- The **event has already occurred before the subject entered** the study, but the exact timing is unknown.
- We only know the event happened **before** a given time.

**Example:**

- A study of HIV diagnosis: some participants are already infected at baseline, but the exact date of infection is unknown.

## 3. Interval Censoring

- The event occurs **within a time interval**, but the exact time is not observed.
- Often arises from periodic follow-up or screening.

**Examples:**

- Cancer detected at a routine annual check-up: the actual onset was between the last negative and first positive test.
- Dental study: tooth loss observed only between check-up visits.

## 4. Type I Censoring (Fixed End Time)

- Study ends at a **pre-specified time**.
- Any subjects still alive/disease-free at that time are right-censored.

**Example:**

- A 5-year clinical trial where patients are followed for exactly 5 years.

## 5. Type II Censoring (Fixed Number of Events)

- Study continues until a **pre-specified number of events** have occurred.
- All other participants still at risk are censored.

**Example:**

- A reliability test where 10 machines are run until 5 failures occur.

## Visual Representation

- **Right censoring**: ───┐ (alive at last follow-up)
- **Left censoring**: ┌─── (event occurred before study entry)
- **Interval censoring**: ┌───┐ (event happened somewhere in between)

## Handling Censoring in Analysis

- Kaplan–Meier and Cox models naturally account for **right censoring**.
- Left and interval censoring require specialized methods:
  - **Turnbull estimator** (generalization of KM for interval censoring).
  - **Parametric survival models** with likelihood-based approaches.
