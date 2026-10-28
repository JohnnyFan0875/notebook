# Understanding the EU AI Act

The EU AI Act is a risk-based regulatory framework for AI systems and certain general-purpose AI models.

Key point: The Act does not treat all AI the same. Its core logic is proportionality: the higher the potential impact on people and society, the stronger the obligations.

## Why the EU AI Act Matters

The Act aims to create an ecosystem of trust around AI by setting harmonized rules for systems that affect safety, rights, and public confidence.

| Goal | Why It Matters |
| --- | --- |
| Build trust | Adoption is easier when users understand the guardrails |
| Harmonize rules | Organizations can work against a more consistent framework |
| Protect people | High-impact systems face stricter obligations |
| Support innovation with limits | Low-risk uses are treated differently from dangerous ones |

## Who It Applies To

The Act reaches beyond one narrow technical role.

| Actor | Typical Role |
| --- | --- |
| Provider | Builds or places an AI system or model on the market |
| Deployer | Uses the AI system in practice |
| Importer or distributor | Helps move the system into the market |

Tip: Governance questions often change depending on whether a team is creating the system, integrating it, or deploying it into a specific workflow.

## Systems vs. Models

The Act distinguishes between AI systems and general-purpose AI models.

| Concept | Meaning |
| --- | --- |
| AI system | A deployable product or workflow with specific inputs, outputs, and use context |
| AI model | A more general underlying model that may power many downstream systems |

Key point: This distinction matters because general-purpose AI can create downstream risk far beyond one product boundary.

## The Risk Pyramid

The Act uses a pyramid-style risk approach.

| Risk Level | Typical Treatment |
| --- | --- |
| Unacceptable risk | Prohibited practices |
| High risk | Allowed only with substantial obligations |
| Limited risk | Transparency or disclosure-focused duties |
| Minimal or no risk | Lighter treatment, though good practice still matters |

This risk-based structure is one reason the Act is frequently discussed alongside responsible AI governance.

## Unacceptable Risk

Some uses are treated as unacceptable because they are considered too harmful or too intrusive.

Examples commonly associated with this tier include:

- subliminal or manipulative practices
- exploitation of vulnerable groups
- social scoring
- certain predictive policing uses
- indiscriminate facial image scraping
- some emotion inference or protected-attribute inference contexts
- certain real-time remote biometric identification scenarios

Warning: Teams should not treat prohibited practices as merely "risky features." They are the kinds of uses that force an early no-go decision.

## High-Risk AI Systems

High-risk systems are not automatically banned, but they face materially stronger obligations because they can affect access, opportunity, safety, or rights.

| High-Risk Area | Why It Is Sensitive |
| --- | --- |
| Biometric systems | Can enable surveillance and identity-related harm |
| Education and employment | Can shape opportunity, selection, and advancement |
| Essential services | Can affect access to credit, healthcare, utilities, or other vital services |
| Law enforcement, migration, asylum, border control | Can strongly affect liberty, due process, and human rights |
| Critical infrastructure | Can affect safety and continuity of important systems |

Key point: The common pattern is impact. These are domains where AI errors or misuse can meaningfully change a person's life chances or safety.

## Limited-Risk and Lower-Risk Systems

Some systems fall into limited-risk or lower-risk categories, where transparency and user awareness matter more than intensive conformity duties.

Typical obligations at lower tiers often focus on:

- disclosure that AI is being used
- clearer user awareness
- proportionate operational controls

Even when the formal burden is lighter, teams still benefit from documenting intended use, known limits, and oversight paths.

## AI Literacy

The Act's logic does not stop at documentation. It also points toward AI literacy for the people who build, integrate, and use AI.

| Audience | Literacy Need |
| --- | --- |
| Builders | Understand model capabilities, limits, and regulatory duties |
| Integrators | Know how to combine models safely in a real workflow |
| Deployers and users | Recognize when AI outputs require challenge, escalation, or human review |

Tip: Literacy is a governance control. A policy is weak if the people operating the system do not understand what the policy is trying to prevent.

## GPAI: General-Purpose AI Models

The Act also includes a separate track for general-purpose AI models because they may power many downstream systems.

| GPAI Concern | Why It Matters |
| --- | --- |
| Broad downstream reuse | One model can shape many other products |
| Scale and power | A single model failure can spread widely |
| Documentation needs | Integrators need enough information to use the model safely |
| Copyright and training content | Training practices can create legal and governance obligations |

Common GPAI obligations include:

1. maintain technical documentation about training and evaluation
2. provide downstream integrators with enough documentation for safe use
3. respect copyright-related obligations
4. summarize training content where required

## Systemic Risk in GPAI

Some GPAI models may cross into systemic-risk territory when their scale or capability creates wider societal or market impact.

Typical systemic-risk style duties include:

- stronger model evaluations
- incident reporting
- cybersecurity expectations
- direct communication with relevant authorities when needed

Warning: Once a model becomes infrastructure for many other systems, "we only ship the base model" is not a sufficient governance mindset.

## Providers vs. Deployers

Responsibility is shared, but not identical.

| Role | Main Question |
| --- | --- |
| Provider | Was the system or model designed, documented, and released with the right controls? |
| Deployer | Is the actual use context appropriate, lawful, and proportionate? |

Key point: A compliant provider does not guarantee a compliant deployment. Real-world use can change the risk profile dramatically.

## Relationship to GDPR and Responsible AI

The EU AI Act and GDPR overlap, but they are not the same.

| Topic | GDPR Focus | EU AI Act Focus |
| --- | --- | --- |
| Personal data | Lawful processing, privacy, rights, and safeguards | May matter when the AI use case processes personal data |
| Risk | Rights and freedoms in data processing | Risk classification of AI uses and obligations by tier |
| Automation | Profiling and automated decision safeguards | Broader governance of AI systems and model use |

The Act is also closely aligned with responsible AI practice because it rewards teams that already do risk classification, documentation, human oversight, and use-case review.

## Minimum Standard Before an AI Act-Sensitive Launch

Before launching or integrating an AI system in a meaningful workflow, you should be able to explain:

1. which risk tier the system belongs to
2. whether the use case touches any prohibited or clearly restricted practices
3. whether the system is high risk and what obligations follow from that
4. whether the deployment relies on a general-purpose AI model and what downstream duties exist
5. who owns provider-side and deployer-side compliance decisions
