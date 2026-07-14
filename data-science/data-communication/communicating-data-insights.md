# Communicating Data Insights

Communicating data insights means turning analysis into a message that a specific audience can understand, trust, remember, and use.

Key point: 洞察本身不會自動產生影響。只有當它被放進對的格式、對的情境、對的敘事裡，才會真正支持決策。

## Start With The Audience

Audience needs should shape the communication before chart selection, wording, or layout decisions.

Useful questions:

- What role does the audience have?
- What do they already know?
- What do they need to know?
- What format do they expect?
- How much trust or familiarity already exists?
- Who is the decision maker?

If you ignore these questions, even correct analysis can fail because the message is either too technical, too vague, or mismatched to the decision context.

Tip: The same analysis may need different versions for operators, managers, and executives.

### Technical vs Non-technical Audiences

One useful distinction is whether the audience is technically informed or non-technical.

- non-technical audiences often need less jargon and more visuals
- technical audiences may tolerate more method detail, but still benefit from clarity
- even non-technical stakeholders may hear technical briefings regularly, so "simple" should not mean patronizing

Another helpful distinction is between operational and strategic communication:

- operational insights often require more technical detail and support day-to-day action
- strategic insights often need less technical depth but higher decision relevance and accountability

## Communication Is More Than The Chart

This course frames communication as a mix of several modes:

- written communication
- visual communication
- verbal communication
- nonverbal communication

Each mode contributes something different:

- written communication creates focus, structure, and supporting explanation
- visual communication makes patterns and comparisons easier to grasp
- verbal communication lets you adapt tone and respond in real time
- nonverbal communication signals whether the message is landing

In practice, strong data communication usually combines several of these instead of relying on a chart alone.

## What A Data Insight Is

An insight is more than a fact or statistic. It is a deeper understanding of a business situation that helps uncover value and guide action.

A practical insight workflow:

1. collect information
2. organize information
3. analyze information
4. determine an action plan
5. communicate the action plan
6. observe the outcome

Key point: If communication and follow-up are missing, the workflow is incomplete. Analysis is only one stage in insight generation.

## Core Principles For Communicating Insights

Several principles appeared repeatedly in the source material:

- tie insights back to business objectives
- do not rely on business context alone; provide enough supporting evidence
- keep the message simple
- break complex insights into smaller ideas
- create a clear focus
- maintain expected formats when possible
- know the subject well enough to explain it in basic terms

These principles all reduce cognitive load for the audience and increase the odds that the message will be used correctly.

If you cannot explain the idea in plain language, the audience may be struggling because the concept is still under-processed, not because they are inattentive.

## Why Visualizations Matter

Visualizations are often the front line of data communication because they:

- simplify large volumes of information
- highlight trends and patterns
- provide a faster route to understanding than raw tables
- help decision makers see a more complete picture than simple aggregates alone

Potential benefits:

- faster decision making
- better decision making
- broader appeal across stakeholders
- easier comparison and pattern detection

Warning: A chart is not automatically informative just because it looks polished. A bad visual can hide structure as easily as it can reveal it.

## Keep Visuals Simple

The notebook version of this topic should stay close to a simple rule: do not ask one chart to do too much.

Practical heuristics:

- prefer simplicity over novelty
- remove nonessential gridlines, decorations, and color noise
- choose a familiar chart form unless there is a strong reason not to
- use complex chart types sparingly
- make incremental changes and gather audience feedback

Ask yourself:

- Is there anything I can remove?
- Does this visual support one main message?
- Am I highlighting trends and patterns, or overwhelming the reader with detail?

## Choose Basic Charts Well

This course used a small set of foundational chart types as the core toolkit:

- bar chart
- histogram
- scatter plot

These are useful because they cover many common questions clearly:

| Chart type | Best for | Common mistake |
| --- | --- | --- |
| Bar chart | Comparing categories | Using it for continuous distributions |
| Histogram | Showing a numeric distribution | Treating it like a category comparison |
| Scatter plot | Showing relationship between two numeric variables | Overlooking overplotting, scale, or outliers |
| Line chart | Showing change over time | Using inconsistent intervals or overloading too many series |

One explicit reminder from the material: bar charts and histograms can look similar, but they answer different questions because they are built for different data types.

Additional chart heuristics:

- if you are tempted to use a pie chart, consider a bar chart first because category comparison usually requires less effort from the audience
- use scatter plots when the main question is the relationship between two quantitative variables
- use line charts when the main question is how performance changes over time

## Visuals Protect Against Misleading Summaries

One of the strongest lessons in the source was that identical summary statistics can hide very different underlying data shapes.

That is why visual exploration matters:

- means and standard deviations may match while patterns differ
- aggregates can conceal clusters, outliers, or nonlinear relationships
- charts can reveal structure that summary tables miss

Tip: If you only report summary statistics, you may accidentally erase the very pattern that matters.

## Story Framing Matters

Data stories work better when they are organized around one problem at a time.

Useful framing rules:

- define the problem in one or two sentences
- avoid trying to investigate multiple problems in one story
- open with the challenge: why are we here?
- make the relevance to the audience explicit early

A strong story opening often contains:

- the problem itself
- the scope of the problem
- the implied method or path for addressing it

## Data Storytelling

Data storytelling is not just "adding words to charts." A useful definition is:

Data storytelling is a method of communicating data insights tailored to a specific audience with an overarching narrative.

Its main advantages:

- easier to understand
- more likely to inspire action
- easier to remember than isolated numbers

The source material also emphasized that stories can increase engagement compared with raw data alone.

## Parts Of A Good Data Story

Three core parts showed up repeatedly:

- visualization: gives the audience a familiar and efficient way to see the pattern
- context: explains why the result matters and how it fits a larger effort
- narrative: gives the data direction, sequence, and meaning

Another helpful phrase from the course was that a story should tell a single insight.

That idea is useful because many weak presentations try to fit every interesting finding into one deck, one dashboard, or one chart. Stronger stories usually revolve around one main message at a time.

Good story text should also stay concise:

- highlight only a few main points
- use clear examples
- move technical details into footnotes or appendix material when possible
- aim for short, high-signal statements rather than dense explanation

## What Makes A Story Stick

Two reasons data stories work well:

- they create engagement
- they improve retention

People tend to remember stories more easily than isolated numbers. This does not mean you should replace evidence with emotion. It means you should package evidence in a form that human attention and memory can handle.

Warning: Emotion should support understanding and action, not distort the evidence. Clarity still comes first.

## Credibility And Trust

Good communication is not just about being noticed. It is also about being believed.

Credibility improves when you:

- keep visual conventions honest
- cite credible sources
- stay consistent in wording and design
- preserve a reputation for integrity over time
- bring in subject matter experts when interpretation needs domain authority

Trust is especially important in data storytelling because the audience is not only receiving information. They are deciding whether to accept the message and act on it.

### Avoid Common Credibility Errors

- avoid truncating the y-axis on bar charts unless you clearly note it
- keep intervals consistent on axes, especially in line charts
- do not use clutter or decoration that makes interpretation harder
- do not use extra colors unless they carry meaning

## A Practical Workflow For Presenting Insights

When preparing a communication deliverable, this sequence works well:

1. identify the audience and desired decision
2. define the single main insight
3. choose the simplest visualization that supports that insight
4. add the business context needed to interpret it
5. write or present a short narrative around the implication
6. remove clutter and test whether the message is still clear
7. gather audience feedback and refine

## Common Failure Modes

- leading with charts before defining the message
- presenting too many insights at once
- using complex visuals to impress rather than clarify
- assuming the audience interprets a chart the same way you do
- forgetting to connect the result back to a business objective
- ignoring audience feedback when a visualization is confusing

## Quick Checklist

Before sharing an insight, check:

- Who is this for?
- What one thing should they remember?
- What action or decision should this support?
- Is the chart type appropriate for the data?
- Can I remove anything unnecessary?
- Have I added enough context for correct interpretation?

## Related Notes

- Start with [Forming Analytical Questions](./forming-analytical-questions.md) before this note if the problem statement is still vague.
- For chart mechanics and plotting workflows, continue into [Visualization](../data-manipulation-and-eda/visualization/README.md).
