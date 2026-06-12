# Core Concepts & Censoring

Survival analysis begins with a different kind of data than standard regression or classification. Before applying any method, you need to understand what survival data looks like, what **censoring** means, and how to structure your dataset correctly.

Key point: The most common mistake: analyzing survival analysis data as a general binary outcome, completely ignoring the "time" dimension and censoring observations. Such an analysis is not only inaccurate, but also wrong in direction.

## The Two Core Variables

Every survival analysis dataset requires exactly two pieces of information per observation:

| Variable | Description | Example |
| ----------------- | --------------------------------------------------------------- | -------------------------------- |
| **Time (T)** | Duration from study entry to the event or censoring | 14.5 months from diagnosis |
| **Event (δ)** | Binary: 1 if the event was observed, 0 if censored | 1 = died, 0 = still alive at end |

This **(T, δ)** pair is the fundamental unit of survival data.

Tip: "Survival" is a historical term — the event does not have to be death. It can be any well-defined, non-repeating event: churn, failure, default, conversion, relapse. The methods work identically regardless of what the event is.

## What Is Censoring?

**Censoring** occurs when the survival time is only partially known. You know the subject survived *at least* until a certain time, but you don't know exactly when (or whether) the event eventually occurred.

This is not missing data — it is **partial information**. Discarding censored observations throws away real data and biases your estimates toward shorter survival times.

### Types of Censoring

| Type | Description | Example |
| ----------------------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| **Right censoring** | Event has not occurred by the end of observation | Patient still alive when study ends (most common) |
| **Left censoring** | Event occurred before observation began — exact time unknown | Infection already present at first blood test |
| **Interval censoring** | Event occurred somewhere between two known time points | Tumor regrowth detected at routine scan |
| **Administrative censoring** | Study ends on a fixed date; survivors are censored at that date | All patients enrolled are censored at study cutoff |
| **Loss to follow-up** | Subject withdraws, moves, or becomes unreachable | Patient stops attending clinic visits |
| **Type I censoring** | Study stops after a pre-specified duration; survivors are censored at that fixed time | 5-year clinical trial: all patients still alive at 5 years are censored |
| **Type II censoring** | Study continues until a target number of events has occurred; remaining subjects are censored | Reliability test runs until 5 of 10 machines fail; remaining 5 are censored |

Warning: Non-informative censoring assumption: Standard survival methods assume that censoring is non-informative — the reason someone is censored is unrelated to their underlying risk of the event. If high-risk individuals are more likely to drop out of the study, the estimates will be biased.

### Right Censoring — The Common Case

```
Subject 1: |----event          (observed event at t=10)
Subject 2: |----------censored (still alive at t=20, study ends)
Subject 3: |------censored     (lost to follow-up at t=14)
Subject 4: |--event            (observed event at t=5)
Subject 5: |-------------censored (still alive at t=26)

Timeline:  0        10        20        26
```

For Subjects 2, 3, and 5: we know they survived *at least* to their censoring time — that information is used, not discarded.

## Data Structure in Python

Survival data in Python (using `lifelines`) requires a **tidy format** with one row per subject, containing at minimum the time and event columns.

```python
import pandas as pd
import numpy as np

# Minimal survival dataset
data = pd.DataFrame({
    'subject_id':   [1,    2,    3,    4,    5,    6,    7,    8],
    'time':         [10,   20,   14,   5,    26,   8,    18,   3 ],
    'event':        [1,    0,    0,    1,    0,    1,    1,    1 ],
    'treatment':    ['A',  'A',  'B',  'B',  'A',  'B',  'A',  'B'],
    'age':          [55,   62,   48,   71,   59,   44,   67,   53]
})

print(data)
print(f"\nEvents observed: {data['event'].sum()} / {len(data)}")
print(f"Censoring rate:  {(1 - data['event'].mean()):.1%}")
```

**Output:**

| time | event | treatment | age |
| ---- | ----- | --------- | --- |
| 10 | 1 | A | 55 |
| 20 | 0 | A | 62 |
| 14 | 0 | B | 48 |
| 5 | 1 | B | 71 |
| 26 | 0 | A | 59 |
| 8 | 1 | B | 44 |

```
Events observed: 5 / 8
Censoring rate:  37.5%
```

### Installing lifelines

```bash
pip install lifelines
```

### Checking Data Quality Before Analysis

```python
import lifelines

# Basic sanity checks
assert (data['time'] > 0).all(),   "All times must be positive"
assert data['event'].isin([0, 1]).all(), "Event must be 0 or 1"
assert data['time'].notna().all(), "No missing times allowed"

print("Data structure check passed.")
print(f"\nTime range:    {data['time'].min()} – {data['time'].max()}")
print(f"Median time:   {data['time'].median()}")
print(f"Events (δ=1):  {data['event'].sum()} ({data['event'].mean():.1%})")
print(f"Censored (δ=0):{(data['event'] == 0).sum()} ({(1-data['event'].mean()):.1%})")
```

## Simulating Realistic Survival Data

For practice and illustration, it is useful to be able to simulate survival data with known properties.

```python
import numpy as np
import pandas as pd

np.random.seed(42)

def simulate_survival(n=200, scale=12, shape=1.5, admin_censor=24, seed=42):
    """
    Simulate survival data from a Weibull distribution.

    Parameters
    ----------
    n           : number of subjects
    scale       : Weibull scale (controls typical survival time)
    shape       : Weibull shape (1 = exponential, >1 = increasing hazard)
    admin_censor: administrative censoring time (study end)
    """
    np.random.seed(seed)

    # True event times from Weibull distribution
    true_times = scale * np.random.weibull(shape, n)

    # Random loss to follow-up (uniform over study period)
    ltfu_times = np.random.uniform(0, admin_censor * 1.5, n)

    # Observed time = min(true event, loss-to-follow-up, admin censoring)
    observed_time = np.minimum(true_times, np.minimum(ltfu_times, admin_censor))

    # Event occurred if observed time equals true event time
    event = (true_times <= ltfu_times) & (true_times <= admin_censor)

    return pd.DataFrame({
        'time':  np.round(observed_time, 2),
        'event': event.astype(int)
    })

df = simulate_survival(n=300, scale=18, shape=1.2, admin_censor=36)
print(df.describe())
print(f"\nEvent rate: {df['event'].mean():.1%}")
```

## Common Data Errors to Avoid

| Error | Why It's Wrong | Fix |
| ------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------- |
| Dropping censored observations | Biases toward shorter observed times; loses real information | Keep all observations; use survival methods |
| Using time=0 for subjects with events at enrollment | Ties at zero cause numerical issues | Ensure all times > 0 |
| Treating survival time as a normal regression outcome | Ignores censoring; assumes constant hazard | Use KM, Cox, or parametric survival models |
| Defining the event ambiguously | Results are uninterpretable if the event definition shifts | Pre-specify event definition before data collection |
| Mixing competing risks without modeling them | Can severely overestimate cumulative incidence | Use competing risks methods (Fine-Gray model) |

Tip: Competing risks: When multiple types of events can occur and experiencing one prevents the other (e.g., dying from cancer vs. dying from heart disease), standard survival analysis overestimates cumulative incidence. The Fine-Gray subdistribution hazard model handles this correctly. Competing risks are an advanced topic, but are very common in real-world data, especially medical research.

Tip: Handling non-right censoring: The Kaplan–Meier estimator and Cox model handle right censoring natively. For left and interval censoring, specialized methods are required: the Turnbull estimator generalizes KM for interval-censored data, while parametric survival models use likelihood-based estimation to incorporate all censoring types.

## Key Takeaways

| Concept | Key Point |
| -------------------------- | --------------------------------------------------------------------------------- |
| **(T, δ) data structure** | Every observation needs a time and a binary event indicator |
| **Right censoring** | The most common type; subject survived at least until their censoring time |
| **Censoring ≠ missing** | Censored observations carry partial information and must not be discarded |
| **Non-informative censoring** | Standard methods require that censoring is unrelated to event risk |
| **Time must be positive** | Ensure all T > 0 before fitting any model |
| **Define the event first** | Ambiguous event definitions make results uninterpretable |
