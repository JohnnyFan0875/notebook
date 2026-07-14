# Association Rules

Association rule mining looks for patterns of items that frequently occur together.

## Topics

- [Apriori](apriori.md)
- [FP-Growth](fp-growth.md)

## Notes

- Common in market basket analysis and transactional data.
- Support, confidence, and lift are the core evaluation quantities.

## Interpretation Reminders

- High support means common, not necessarily useful.
- High confidence may simply reflect a very common right-hand-side item.
- Lift is often the better first check because it compares against a chance baseline.

[Back to Unsupervised Learning](../README.md)
