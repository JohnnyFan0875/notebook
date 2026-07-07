# GitHub Concepts

## Git vs GitHub

Git is the version control system. GitHub is a collaboration platform built around Git repositories, hosting, review workflows, and repository policies.

## Repository Collaboration Basics

Common collaboration units on GitHub include:

| Concept | Purpose |
| --- | --- |
| Repository | Shared project home for code, issues, and history |
| Branch | Isolated line of work |
| Pull request | Proposed set of changes for discussion and merge |
| Review | Feedback and approval process before integration |
| Branch protection | Rules that restrict direct changes to important branches |

## Branches on GitHub

Branches help teams work in parallel while reducing direct interference.

- The default branch is often `main`.
- New work is typically done on feature branches.
- Branches can be compared before merging.

This supports safer experimentation and clearer review.

## Pull Requests

A pull request is not just a merge button. It is the unit of review and discussion.

Typical purposes:

- explain why a change exists
- show the diff against a target branch
- request feedback
- gate merging behind review or CI checks

Good pull requests are usually focused, scoped, and readable.

## Branch Protection Rules

GitHub can enforce rules on important branches such as:

- requiring pull requests before merging
- requiring approvals
- requiring passing status checks
- preventing direct pushes

These controls reduce accidental breakage and make collaboration more predictable.

## Practical Workflow

1. Create a feature branch.
2. Commit work locally.
3. Push the branch to GitHub.
4. Open a pull request.
5. Address review feedback and checks.
6. Merge into the protected target branch.

## Practical Takeaways

- Git handles history; GitHub structures team collaboration around that history.
- Branches isolate work, and pull requests make changes reviewable.
- Protected branches are workflow safeguards, not bureaucracy for its own sake.
- Strong GitHub habits improve code quality, traceability, and team coordination.
