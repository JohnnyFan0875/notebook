# Loan Amortization

## Core Idea

A loan amortization table shows how a fixed-term loan is paid down over time through periodic payments that contain both interest and principal.

## What an Amortization Table Answers

An amortization schedule helps answer:

- how much each payment will be
- how much of each payment goes to interest
- how much goes to principal
- how the remaining balance changes over time

## Where It Commonly Applies

Amortization tables are most common for loans with structured repayment schedules, such as:

- mortgages
- car loans
- student loans

They are less natural for products such as revolving credit cards or open lines of credit, where balances and payment behavior are more variable.

## Main Elements

A standard amortization table usually includes:

| Field | Meaning |
| --- | --- |
| Period | Payment number or date |
| Beginning balance | Outstanding balance before the payment |
| Payment | Total amount paid that period |
| Interest portion | Amount allocated to interest |
| Principal portion | Amount allocated to principal |
| Ending balance | Outstanding balance after the payment |

## Why the Table Changes Over Time

In a standard amortizing loan:

- early payments often have a larger interest share
- later payments usually have a larger principal share
- the total balance declines until it reaches zero at the end of the term

This is why two payments of the same total amount may have very different internal composition depending on when they occur.

## Spreadsheet Usefulness

Spreadsheets are a good fit for amortization because they make it easy to:

- parameterize loan amount, rate, and term
- inspect period-by-period breakdowns
- model alternative scenarios
- compare repayment schedules visually

## Practical Modeling Considerations

When building an amortization model, define clearly:

- the loan principal
- annual interest rate
- payment frequency
- number of periods
- whether extra payments are allowed

Small setup errors in rate conversion or period counts can distort the whole schedule.

## Practical Takeaways

- Amortization is about the time path of principal repayment plus interest allocation.
- The same payment amount can shift from mostly interest to mostly principal over the life of the loan.
- Spreadsheets are useful because they make repayment mechanics transparent and easy to scenario-test.
