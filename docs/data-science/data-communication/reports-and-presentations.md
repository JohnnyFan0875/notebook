# Reports and Presentations

Reports and presentations are the delivery layer of data communication. After the question is framed and the insight is clarified, you still need to decide what to show, what to leave out, and which format best supports the audience's decision.

Key point: 好的分析不只要「說得懂」，還要「交付得對」。同一組分析結果，交給 technical colleague、manager、customer 的形式可能完全不同。

## Start With The Delivery Question

Before building a report, deck, or memo, clarify four things:

1. who is the audience
2. what is the purpose
3. what is the main message
4. what format best fits the situation

This is the practical planning layer that sits between insight generation and final communication.

## Use Personas To Guide Selection

Persona thinking helps decide what level of detail belongs in the deliverable.

Questions to ask:

- Is the audience technical, non-technical, or mixed?
- Are they making a strategic decision or handling an operational task?
- How much background do they already have?
- How much time do they have?
- Are they the decision maker, reviewer, or implementer?

Tip: Different personas should often get different findings, not just different wording.

## Select Findings, Not Everything

A common mistake is trying to present every result that came out of the analysis. Stronger communication selects only the findings that support the main point.

Useful rules:

- include the minimal amount of information needed to support the story
- prioritize relevant findings over interesting side results
- use statistics only when they help interpretation
- tailor the depth of detail to the audience

For example:

- a general audience may need the business meaning of a result
- a technical audience may also need method details, assumptions, and limitations

Warning: Data abundance often causes message dilution. More results do not automatically produce more clarity.

## Match The Format To The Goal

Different communication goals imply different formats.

| Purpose | Typical use | Best-fit format |
| --- | --- | --- |
| Informative | Share current status or findings | Summary report, dashboard review, short presentation |
| Instructional | Explain process or method | Technical report, workshop, walkthrough |
| Persuasive | Drive action or change | Executive memo, decision deck, recommendation presentation |

The choice of format should follow the decision context, not personal preference.

## Choose Between Written Reports And Presentations

Written reports and oral presentations solve different problems.

| Format | Best when | Main strength |
| --- | --- | --- |
| Written report | The reader may revisit details later | Precision, completeness, reproducibility |
| Presentation | The audience needs guided attention in real time | Focus, pacing, persuasion, interaction |

In many real settings, the two should support each other rather than compete:

- the report preserves detail
- the presentation drives attention to the key message

## Written Reports

A written report should be clear, precise, and reproducible.

Key qualities:

- readable by the intended audience
- explicit about context and findings
- structured enough to be scanned
- reproducible and properly sourced

### Common Report Types

| Report type | Focus | Typical audience |
| --- | --- | --- |
| Summary report | Key findings and recommendations | Managers, executives, busy stakeholders |
| Final or analytical report | Full analysis, method, interpretation, evidence | Technical stakeholders, reviewers, project archive |
| Informational report | Status or descriptive information | Operational teams, monitoring use cases |

### Summary Report Structure

A practical summary report can often be organized as:

1. contextual information
2. key findings
3. interpretation
4. recommendations or next steps

The point is not to reproduce the entire analysis. The point is to make the most important conclusions retrievable quickly.

### Analytical Report Structure

An analytical or final report usually needs more depth:

1. problem and background
2. data and methods
3. analysis and results
4. interpretation
5. limitations
6. conclusions and recommendations
7. references or appendix

Tip: Many readers scan the introduction and conclusion first. Make sure those sections stand on their own.

## Reproducibility Belongs In Communication

Reproducibility is not separate from reporting quality. If a result cannot be traced, checked, or recreated, the communication is weaker even if the writing sounds polished.

A reproducible report should make it possible to answer:

- Where did the data come from?
- What transformations were applied?
- What method or model was used?
- What assumptions were made?
- How can someone locate the sources?

Helpful practices:

- cite data sources and publications
- name datasets, time windows, and variables clearly
- separate findings from interpretation
- make supporting information available and retrievable

## Executable Reports And Literate Analysis

Some reporting workflows go beyond static documents and combine narrative, code, figures, and metadata in one reproducible artifact.

Common examples include:

- R Markdown
- Quarto
- Jupyter-based reporting workflows

The tool matters less than the operating idea:

- analysis and explanation live together
- figures are regenerated from code instead of pasted manually
- document metadata controls title, author, date, and output format
- the same source can sometimes render to multiple outputs

This approach is especially useful when a report needs to stay:

- reproducible
- updateable
- reviewable by technical collaborators

Tip: If a report is regenerated repeatedly for new time windows, regions, or segments, parameterized reporting is often better than copying and editing slides or docs by hand.

## Write Precisely And Clearly

Good reports reduce ambiguity.

Practical habits:

- prefer direct sentences over decorative phrasing
- define the point before expanding on it
- remove statements that add no information
- explain technical terms when the audience may not know them
- keep recommendations specific enough to act on

If a sentence cannot help the reader understand, decide, or verify, it probably does not belong.

## Plan Presentations Before Building Slides

Do not start with slides. Start with structure.

A simple planning frame:

- purpose
- audience
- message

This is often enough to prevent slide sprawl and unclear pacing.

## Presentation Types

Presentations often fall into three broad types:

- informative: explain what is happening
- instructional: explain how something works
- persuasive: argue for action or change

Knowing which one you are giving changes the content mix, tone, and call to action.

## Define The Central Message

The audience will forget most details. The message should therefore be compressible into one sentence.

Useful framing:

- opening statement: catches attention
- central message: the core takeaway
- closing statement: reinforces the takeaway and next step

Example pattern:

- opening: negative ratings are hurting the business
- central message: delayed shipping is the main driver
- closing: immediate action is needed to reverse the trend

Key point: If the message cannot fit into one sentence, the presentation is probably trying to do too much.

## Presentation Structure

A simple presentation structure works in many cases:

1. introduction
2. methods, analysis, and outputs
3. conclusions and takeaways

The introduction should:

- provide background
- catch attention
- preview what is coming

The ending should:

- return to the opening problem
- summarize the takeaway
- include next steps or a call to action when appropriate

## Keep The Outline Tight

Aim for a small number of sections. The source material suggested five or fewer smaller parts, which is a good practical ceiling for many presentations.

A workable outline might be:

1. reason for the analysis
2. exploratory analysis
3. core model or method
4. conclusions
5. follow-up actions

## Build Better Slides

Slides should support the story, not replace it.

Useful heuristics:

- one message per slide
- keep slides short and dynamic
- judge slide quality by clarity, not by slide count
- use visuals to support the spoken narrative

Warning: Slide count and timing are weak quality metrics. A short deck can still be confusing, and a longer deck can still be coherent.

## Design Choices That Affect Readability

Color and layout choices influence comprehension directly.

Practical rules:

- use color to convey meaning, not decoration
- keep good contrast between text and background
- avoid relying on red and green combinations
- keep the palette limited, often no more than three main colors
- design for inclusive readability, including color-vision deficiencies

## Handling Time And Audience Size

Presentations should adapt to logistics as well as content.

Consider:

- small meeting vs large conference
- workshop vs executive update
- short slot vs extended session

These affect:

- level of detail
- number of examples
- interactivity
- time available for questions

## A Practical Delivery Workflow

Use this sequence when preparing a deliverable:

1. identify audience persona
2. define purpose and decision context
3. write the main message in one sentence
4. select only the findings that support that message
5. choose the right format
6. structure the report or presentation
7. add supporting visuals and evidence
8. verify clarity, credibility, and reproducibility

## Common Failure Modes

- mixing multiple problems into one deliverable
- choosing findings because they are interesting rather than relevant
- overloading non-technical audiences with technical detail
- hiding method details when technical review is required
- treating slide count as a quality metric
- writing reports that cannot be traced back to data and method

## Quick Checklist

Before sharing a report or presentation, ask:

- Who is this for?
- What decision should this support?
- What is the one-sentence message?
- Did I include only the findings needed for that message?
- Is the format appropriate?
- Is the result clear, precise, and reproducible?

## Related Notes

- Start with [Forming Analytical Questions](./forming-analytical-questions.md) when the problem is still vague.
- Continue with [Communicating Data Insights](./communicating-data-insights.md) for audience, story, and visualization principles.
