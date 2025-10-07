# Types of Censoring in Survival Analysis

In survival analysis, **censoring** occurs when the exact time of an event (e.g., death, relapse, failure) is **not fully observed**.

- Censoring does not mean the subject had no event — rather, it indicates that **information about their event time is incomplete**.
- Properly handling censoring is fundamental to obtaining unbiased estimates of survival probability and hazard.
- A censored subject contributes to the risk set up until the time of censoring. After that, they are removed from the risk set, but they do not count as an event.
- The curve does **not drop** at censoring times (since no event occurred), but the **risk set decreases**.

## 1. Right Censoring (Most Common)

> The event has **not yet occurred** by the end of observation.

This is the default form of censoring in most clinical and reliability studies.

- The participant is still alive or event-free at study end.
- The participant withdrew or was lost to follow-up before experiencing the event.

**Example**

- A patient remains alive at the last follow-up visit.
- A participant drops out midway through the study.

**Notation**

\[
T_i = \min(\text{event time}, \text{censoring time}), \quad
\delta_i =
\begin{cases}
1, & \text{if event observed} \\
0, & \text{if censored}
\end{cases}
\]

## 2. Left Censoring

> The event has already occurred **before** the subject entered the study,  
> but the exact timing is **unknown**.

- We only know the event happened earlier than a certain time point.

**Example**

- In an HIV cohort, some participants are already infected at baseline,  
  but their exact date of infection is unknown.

## 3. Interval Censoring

> The event occurs **within a time interval**, but the precise time is unobserved.

This typically arises in studies with **periodic follow-up or screening**.

**Examples**

- A tumor is detected at an annual exam; the actual onset was between the last negative and the first positive test.
- Tooth loss is observed only between dental check-ups.

## 4. Type I Censoring (Fixed End Time)

> The study stops after a **pre-specified duration**.

- Subjects who remain event-free at that time are right-censored.

**Example**

- A 5-year clinical trial: all participants still alive at 5 years are censored at that point.

## 5. Type II Censoring (Fixed Number of Events)

> The study continues until a **target number of events** has occurred.

- All remaining participants are censored once the required number of events is reached.

**Example**

- A reliability test runs 10 machines until 5 have failed;  
  the remaining 5 are right-censored.

## 6. Visual Summary

| Censoring Type | Description                       | Representation                 |
| -------------- | --------------------------------- | ------------------------------ |
| **Right**      | Event not observed during study   | ───┐ (alive at last follow-up) |
| **Left**       | Event occurred before study entry | ┌───                           |
| **Interval**   | Event known to occur within range | ┌───┐                          |

## 7. Handling Censoring in Analysis

- **Kaplan–Meier estimator** and **Cox proportional hazards models** naturally account for **right censoring**.
- **Left** and **interval** censoring require specialized approaches:
  - **Turnbull estimator** (generalization of KM for interval-censored data)
  - **Parametric survival models** with likelihood-based estimation

## Key Points

- Censoring ≠ missing data — censored subjects still contribute information up to their censoring time.
- Right censoring is by far the most common in clinical and genomic studies.
- Understanding censoring types is essential before model fitting or survival-curve interpretation.

> Correctly specifying censoring ensures valid estimation of survival probabilities and unbiased hazard ratios.
