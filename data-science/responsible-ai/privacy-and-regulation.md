# Privacy and Regulation

> **待改寫（補內容）**：補 HIPAA（PHI、Safe Harbor vs Expert Determination de-identification）、基因資料的再識別風險，以及 dbGaP / EGA 等受控存取（controlled access）與 Data Use Agreement。

本篇三部分：隱私的基本概念與 privacy by design、GDPR（合法基礎、data subject rights、DPIA、自動化決策）、資料安全（分類、控制措施、NIST CSF、社交工程）。匿名化實作見 [Anonymization in Python](anonymization-in-python.md)。

## Data Privacy

Data privacy focuses on how personal data is collected, used, shared, protected, and controlled.

Key point: Privacy is not only about secrecy. It is about meaningful control over personal data and clear limits on how organizations can use it.

### What Privacy Means

At a high level, privacy is often framed as the right to be left alone. In modern data systems, that idea extends into control over how personal information is collected and processed.

| Privacy Question | Why It Matters |
| --- | --- |
| What counts as personal data? | Organizations need to know what requires stronger protection |
| Who controls the data? | People should not lose all agency once data is collected |
| How is the data used? | Secondary use often creates the biggest privacy gap |
| What happens if misuse occurs? | Harm can persist long after the original collection event |

### Personal Data

Personal data is any data related to an identified or identifiable person.

Common examples include:

- name
- date of birth
- geolocation
- contact details
- behavioral and engagement data tied back to a user

Tip: Privacy risk often comes from combinations of fields, not only obviously sensitive columns. Several harmless-looking attributes together can identify a person.

### Why Privacy Has Become More Complex

Privacy concerns expanded sharply in the 21st century because people leave larger digital footprints across the internet, apps, platforms, and connected devices.

| Modern Driver | Privacy Concern |
| --- | --- |
| Apps and cloud services | Constant background data collection |
| Big data analytics | Large-scale inference about users |
| Cross-platform tracking | Profiles built across contexts |
| Surveillance capabilities | Persistent observation without meaningful awareness |

Warning: Users often do not understand the full extent of what is collected, inferred, purchased, or shared about them.

### Privacy vs. Security

Privacy and security are related, but they are not identical.

| Concept | Focus |
| --- | --- |
| Privacy | Whether data collection and use are justified, controlled, and respectful of individuals |
| Security | Whether data is protected from unauthorized access, alteration, disruption, or destruction |

Key point: Strong security does not automatically make a data practice private. A company can store data securely and still collect too much or use it in ways users would not expect.

### A Simple Security Foundation: CIA Triad

Privacy programs often depend on basic security controls. A common security model is the CIA triad:

| Element | Meaning |
| --- | --- |
| Confidentiality | Only the right people and systems can access the data |
| Integrity | Data is not improperly altered or corrupted |
| Availability | Data and systems remain usable when needed |

Confidentiality is especially important for privacy because it limits unnecessary access to personal information.

### How Companies Use User Data

Organizations collect more than one kind of data about users.

| Data Type | Example Use |
| --- | --- |
| Personal data | Account management or identity-related functions |
| Engagement data | Understanding how users interact with a product |
| Behavioral data | Tracking actions, habits, or patterns |
| Attitudinal data | Surveys, reviews, preferences, and opinions |

Typical business motivations include:

1. product and user-experience improvement
2. targeted advertising and profiling
3. data brokerage or resale
4. broader business strategy and investment decisions

Warning: The same data collected for convenience or personalization can later be reused for profiling, targeted selling, or pricing discrimination.

### When Privacy Goes Wrong

Privacy failures can harm users directly.

| Failure Pattern | Possible Harm |
| --- | --- |
| Information stolen | Identity theft or fraud |
| Over-sharing or resale | Sensitive profiles exposed to third parties |
| Aggressive targeting | Manipulative advertising or unwanted inference |
| Differential treatment | Pricing discrimination or exclusion |

The "privacy paradox" adds a real challenge: people often express concern about privacy while still using data-intensive services because convenience and social dependence are hard to avoid.

### Privacy by Design

Privacy should be built into products and workflows from the start rather than added after a complaint or regulatory problem.

| Privacy-by-Design Idea | Practical Meaning |
| --- | --- |
| Build privacy early | Include privacy requirements during design, not after launch |
| Keep users at the center | Make choices understandable and usable |
| Fit naturally into the interface | Privacy controls should not feel hidden or obstructive |
| Use timely notice | Explain collection at the moment it becomes relevant |

Tip: A good privacy interface should feel natural, not clunky. People make better choices when the request appears at the right time, in the right context, and with clear options.

### Just-in-Time Notice

Just-in-time notices present privacy information exactly when a user is about to share data or trigger a new type of collection.

This approach is useful because:

- users are more likely to notice it
- the context is clearer than in a long policy document
- laws and user expectations increasingly favor timely explanation

### Data Classification and Privacy Risk

Organizations need a structure for classifying data so they can manage privacy and security proportionately.

| Classification Question | Why It Matters |
| --- | --- |
| Is this personal or sensitive data? | Higher sensitivity usually requires stronger controls |
| Who should access it? | Limits internal misuse and accidental exposure |
| How long should it be retained? | Reduces unnecessary long-term risk |
| Can it be shared externally? | Forces review of jurisdiction, consent, and policy fit |

Key point: Classification is the basis for organizing, managing, and protecting data. Without it, privacy controls become inconsistent and reactive.

### Minimum Standard for a Privacy Program

Before collecting or reusing personal data, you should be able to explain:

1. what kinds of user data are being collected
2. why each category is necessary
3. who can access the data and under what controls
4. how users are informed and what choices they have
5. what harms could occur if the data is misused, breached, or resold

## GDPR

The General Data Protection Regulation (GDPR) is the European Union's core framework for personal data protection and lawful processing.

Key point: GDPR is not just a privacy notice requirement. It is a full operating framework for how organizations collect, justify, use, protect, and govern personal data.

### Why GDPR Matters

GDPR is designed to protect privacy as a fundamental right in the digital age while creating a more harmonized data protection framework across the EU and EEA.

| GDPR Goal | Why It Matters |
| --- | --- |
| Protect individuals' rights | Personal data is tied to dignity, autonomy, and control |
| Harmonize rules | Organizations avoid fragmented country-by-country logic inside the EU framework |
| Increase transparency | People should understand how their data is used |
| Create accountability | Organizations must demonstrate, not merely claim, compliance |

### Scope

GDPR applies to personal data relating to natural persons and covers both automated processing and certain structured manual processing.

| Scope Question | GDPR View |
| --- | --- |
| Whose data is protected? | Data subjects who are natural persons |
| What counts as personal data? | Data that identifies or can identify a person directly or indirectly |
| Which processing is covered? | Collection, storage, analysis, sharing, retrieval, erasure, and more |
| Is it only about EU-based companies? | No. The reach can extend beyond the EU when EU personal data is involved |

Tip: GDPR scope is broader than many teams expect. "We are not based in Europe" is not, by itself, a safe compliance shortcut.

### Personal Data and Special Categories

GDPR treats some data as especially sensitive.

| Category | Examples |
| --- | --- |
| General personal data | Name, contact details, location, account-linked behavior |
| Special category data | Health, biometric data, political or religious beliefs, sexuality, union membership |

Sensitive data and vulnerable populations usually trigger stronger obligations and closer scrutiny.

### Core GDPR Principles

These principles are the backbone of GDPR thinking.

| Principle | Practical Meaning |
| --- | --- |
| Lawfulness, fairness, and transparency | Processing must have a legal basis, be fair, and be explainable |
| Purpose limitation | Data should be collected for specific purposes and not reused incompatibly |
| Data minimization | Collect and process only what is adequate, relevant, and necessary |
| Accuracy | Keep data correct and up to date |
| Storage limitation | Do not retain personal data longer than justified |
| Integrity and confidentiality | Use appropriate security and access controls |
| Accountability | Controllers must implement and demonstrate compliance |

Warning: These principles work together. A project can fail GDPR expectations even if it is strong on one principle but weak on purpose, minimization, or accountability.

### Roles: Controller and Processor

GDPR distinguishes who decides the purpose of processing from who handles data on behalf of others.

| Role | Main Responsibility |
| --- | --- |
| Controller | Decides why and how personal data is processed |
| Processor | Processes personal data on behalf of a controller |

Key point: Accountability primarily sits with the controller, especially for showing that the principles above are actually implemented.

### Legal Bases for Processing

Personal data processing needs a valid legal basis.

| Legal Basis | Typical Idea |
| --- | --- |
| Consent | Clear, informed, freely given agreement |
| Contract | Processing is necessary to perform a contract |
| Legal obligation | Processing is required by law |
| Vital interests | Processing protects someone's life or safety |
| Public task | Processing supports an official or public-interest task |
| Legitimate interests | A reasonable and necessary interest balanced against the subject's rights |

Tip: Consent is important, but it is not the only legal basis. Teams often over-assume consent when another basis may be more accurate or when consent would not be freely given.

### Data Subject Rights

GDPR gives individuals rights over their data.

Common rights include:

1. the right to be informed
2. the right of access
3. the right to rectification
4. the right to erasure in certain cases
5. the right to object or restrict certain processing

Fairness and transparency depend heavily on whether these rights can be exercised in practice rather than only described on paper.

### Purpose Limitation and Data Minimization

Two of the most practical GDPR habits are:

- define the purpose before collecting the data
- avoid collecting data "just in case"

| Principle | Bad Habit It Prevents |
| --- | --- |
| Purpose limitation | Reusing data for unrelated secondary purposes |
| Data minimization | Collecting excessive data because storage is cheap |

### Security and Integrity

GDPR expects appropriate organizational and technical measures to protect personal data.

| Measure Type | Examples |
| --- | --- |
| Organizational | Training, policies, role clarity, accountability, risk assessment |
| Technical | Access control, secure storage, encryption, pseudonymization, device and network protections |

Key point: Security is not separate from GDPR. Integrity and confidentiality are one of its core principles.

### DPIA: Data Protection Impact Assessment

A DPIA is used when processing is likely to create high risk for rights and freedoms.

| DPIA Focus | What It Asks |
| --- | --- |
| Context and scope | What is being processed, at what scale, and for what purpose? |
| Risk to people | What negative consequences could affect rights, dignity, or safety? |
| Mitigation | Which controls reduce those risks? |
| Residual risk | What risk remains after mitigation? |

High-risk signals often include:

- large-scale processing
- sensitive or biometric data
- systematic monitoring
- combined datasets
- vulnerable data subjects
- automated decision-making
- use of new technologies

Tip: Even when not strictly required, DPIA-style thinking is a strong habit for responsible AI and privacy-sensitive systems.

### GDPR and AI

GDPR does not function as an AI law, but it creates important constraints for AI projects that process personal data.

| AI Concern | GDPR Relevance |
| --- | --- |
| Large-scale data processing | Raises minimization, security, and proportionality questions |
| Profiling | Triggers fairness, transparency, and sometimes special safeguards |
| Black-box behavior | Makes explanation and accountability harder |
| Sensitive inference | Can raise discrimination and special category issues |

GDPR compliance for AI projects often depends on:

- lawful basis
- transparency
- data minimization
- accountability
- security
- DPIA or comparable risk review

### Automated Decision-Making and Profiling

Profiling means analyzing personal data to evaluate or predict aspects of a person's behavior, preferences, status, or likely actions.

Article 22 is especially important in this area because it addresses certain automated individual decisions, including profiling, and points toward safeguards such as human intervention and explanation.

Warning: If an AI system makes or strongly shapes individual decisions, teams should not treat profiling as a minor analytics feature. It can be a high-stakes compliance and ethics issue.

### Minimum Standard Before a GDPR-Sensitive Project Launches

Before launching a system that processes personal data, you should be able to explain:

1. what personal data is processed and why
2. which legal basis justifies that processing
3. how the GDPR principles are implemented in practice
4. whether a DPIA or equivalent risk review is needed
5. what rights, safeguards, and human review paths exist for affected people

## Data Security

Data security is the practice of protecting digital information from unauthorized access, disclosure, alteration, or destruction.

Key point: Data security is not only a technical control problem. It also depends on classification, access decisions, training, incident readiness, and organizational culture.

### Why Data Security Matters

Weak security creates operational, legal, and reputational harm long before a breach becomes a headline.

| Risk | Why It Matters |
| --- | --- |
| Unauthorized access | Sensitive records can be exposed or misused |
| Data alteration | Reports, models, and operational systems become unreliable |
| Data loss or destruction | Critical business processes can stall or fail |
| Compliance failure | Legal exposure, fines, and mandatory remediation increase |
| Trust erosion | Customers and partners lose confidence after incidents |

Tip: The cost of weak security is rarely limited to one compromised dataset. It often spreads into customer trust, regulatory scrutiny, and long cleanup programs.

### Data Sensitivity and Classification

Security becomes more practical when organizations classify data by impact and sensitivity.

| Example Level | Practical Meaning | Example Content |
| --- | --- | --- |
| Public | Intended for broad sharing and low-impact exposure | Public website content, marketing material |
| Internal | For employees or trusted partners only | Meeting notes, internal policies |
| Confidential | Private data needing stronger restriction | Customer phone numbers, bank details, strategic plans |
| Highly confidential or restricted | Severe impact if exposed | Government intelligence, scientific research, highly sensitive identifiers |

Key point: Classification is not just labeling. It determines who should access data, how it should be stored, and what controls are required.

### Personally Identifiable Information

`PII` deserves special attention because misuse can directly harm individuals.

| PII Concern | Why It Matters |
| --- | --- |
| Identity exposure | Can enable fraud, impersonation, or targeted abuse |
| Compliance obligations | Often triggers stricter legal and reporting duties |
| Higher business impact | Breaches involving PII usually create stronger reputational damage |

What teams should know at a minimum:

1. the organization’s classification levels
2. who may access each level
3. what counts as `PII`
4. how sensitive data must be handled
5. how to report a suspected breach

### Compliance and Security Requirements

Security obligations can come from both law and regulatory bodies.

| Requirement Type | Meaning |
| --- | --- |
| Legal requirement | Mandated by law |
| Mandatory regulatory requirement | Required by a regulator or industry authority |
| Voluntary framework | Not legally binding, but useful for structure and maturity |

Common compliance themes include:

1. data minimization
2. purpose limitation
3. data subject rights
4. data protection controls
5. breach notification expectations

Warning: Meeting the minimum legal requirement does not automatically mean the organization is secure enough for its real threat environment.

### Voluntary Frameworks

Organizations often use voluntary frameworks to create a more proactive security program.

| Framework | Typical Use |
| --- | --- |
| `NIST CSF` | Organize cybersecurity risk management with a common operating language |
| `ISO 27001` | Build and audit a formal information security management system |
| `COBIT` | Align governance, controls, and enterprise IT management |

#### NIST CSF at a Glance

The extracted material emphasized the classic `NIST CSF` flow:

| Function | Main Question |
| --- | --- |
| Identify | What assets, dependencies, and risks matter most? |
| Protect | Which safeguards reduce the likelihood of harm? |
| Detect | How will we notice suspicious activity or control failure? |
| Respond | What do we do once an incident is underway? |
| Recover | How do we restore service and learn from the event? |

Tip: A framework is most useful when it creates a repeatable security rhythm, not when it becomes a documentation exercise.

### Core Security Controls

Most data security programs rely on a recurring set of controls.

| Control Area | Practical Examples |
| --- | --- |
| Access control | Least privilege, role-based access, approval workflows |
| Authentication | Strong passwords, MFA, credential hygiene |
| Encryption | Protection for data at rest and in transit, key management |
| Data loss prevention | Restrict or monitor risky exfiltration paths |
| Backup and recovery | Tested restoration procedures for critical data and systems |
| Incident response | Defined escalation and communication process during an event |
| Patch and vendor management | Regular updates and third-party review |

Key point: Encryption is powerful, but it does not replace access control, incident response, or training.

### Social Engineering Risk

Many security incidents start by exploiting people rather than breaking software directly.

| Technique | Practical Meaning |
| --- | --- |
| Phishing | Pretending to be a trusted source to steal actions or credentials |
| Smishing | Phishing over SMS or messaging channels |
| Vishing | Voice-based phishing |
| Spear phishing | Targeted phishing using specific knowledge about the victim |
| Whaling | Targeting executives or high-value roles |
| Business email compromise | Manipulating business communication for money or access |
| Baiting | Using a tempting offer or object to trigger unsafe action |
| Pretexting | Creating a false story to gain trust and extract information |
| Piggybacking | Following someone physically into a restricted area |
| Scareware | Using fear-based prompts to pressure a rash response |

#### Common Red Flags

People should slow down when they see:

1. urgent or threatening language
2. unprofessional or inconsistent communication
3. suspicious links or attachments
4. unusual requests for sensitive information

Tip: Social engineering defense starts with permission to pause, verify, and escalate without embarrassment.

### Reactive vs Proactive Security

Security programs often fail when they only react after something has already gone wrong.

| Reactive Pattern | Proactive Pattern |
| --- | --- |
| Focus on known incidents only | Assess known and emerging threats continuously |
| Follow minimum requirements | Add controls based on actual business risk |
| Act after damage appears | Audit, patch, train, and test ahead of time |
| Depend on post-incident cleanup | Build resilience before incidents happen |

Ways to be proactive include regular audits, third-party review, patching, technical best practices, and continuous training.

### Common Pitfalls

The source material repeatedly returned to the same failure modes.

| Pitfall | Why It Hurts |
| --- | --- |
| No clear strategy | Controls become fragmented and inconsistent |
| Inadequate training | People become the easiest attack path |
| Poor data classification | Sensitive data is not protected proportionately |
| Weak incident response plan | Teams react slowly and inconsistently during breaches |
| Overreliance on tools | Process and judgment gaps stay hidden |
| Failure to update policies | Controls drift away from current threats and systems |
| Ignoring insider threats | Authorized access is treated as inherently safe |

Warning: Overly complex security measures can backfire if people cannot follow them consistently in real work.

### Security Culture and Communication

Strong security depends on communication, not only enforcement.

| Cultural Need | Why It Matters |
| --- | --- |
| Shared responsibility | People treat security as part of the job |
| Low-friction reporting | Suspicious events are surfaced early |
| Practical communication | Teams know what to report, when, and to whom |
| No fear of escalation | People are more likely to report mistakes quickly |

Key point: A security culture works best when people feel responsible for protecting data without fear of punishment for raising concerns early.

### Minimum Standard for a Healthy Data Security Practice

Before calling a data security program credible, you should be able to explain:

1. how the organization classifies sensitive data and `PII`
2. which controls protect confidentiality, integrity, and availability
3. how access, encryption, backup, and incident response are handled
4. how social engineering risk is reduced through training and process
5. how the program stays proactive instead of reacting only after breaches
