# Communicating Results

分析結果要產生影響，得經過兩步：先把洞察整理成受眾能理解、信任、記住的訊息（audience、視覺化、data story、credibility），再選對交付形式（書面報告、簡報、可重現報告）。

Key point: 好的分析不只要「說得懂」，還要「交付得對」；而對技術讀者來說，「可重現」本身就是溝通品質的一部分。

## Communicating Insights

Communicating data insights means turning analysis into a message that a specific audience can understand, trust, remember, and use.

Key point: 洞察本身不會自動產生影響。只有當它被放進對的格式、對的情境、對的敘事裡，才會真正支持決策。

### Start With The Audience

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

#### Technical vs Non-technical Audiences

One useful distinction is whether the audience is technically informed or non-technical.

- non-technical audiences often need less jargon and more visuals
- technical audiences may tolerate more method detail, but still benefit from clarity
- even non-technical stakeholders may hear technical briefings regularly, so "simple" should not mean patronizing

Another helpful distinction is between operational and strategic communication:

- operational insights often require more technical detail and support day-to-day action
- strategic insights often need less technical depth but higher decision relevance and accountability

### Communication Is More Than The Chart

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

### What A Data Insight Is

An insight is more than a fact or statistic. It is a deeper understanding of a business situation that helps uncover value and guide action.

A practical insight workflow:

1. collect information
2. organize information
3. analyze information
4. determine an action plan
5. communicate the action plan
6. observe the outcome

Key point: If communication and follow-up are missing, the workflow is incomplete. Analysis is only one stage in insight generation.

### Core Principles For Communicating Insights

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

### Why Visualizations Matter

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

### Keep Visuals Simple

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

### Choose Basic Charts Well

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

### Visuals Protect Against Misleading Summaries

One of the strongest lessons in the source was that identical summary statistics can hide very different underlying data shapes.

That is why visual exploration matters:

- means and standard deviations may match while patterns differ
- aggregates can conceal clusters, outliers, or nonlinear relationships
- charts can reveal structure that summary tables miss

Tip: If you only report summary statistics, you may accidentally erase the very pattern that matters.

### Story Framing Matters

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

### Data Storytelling

Data storytelling is not just "adding words to charts." A useful definition is:

Data storytelling is a method of communicating data insights tailored to a specific audience with an overarching narrative.

Its main advantages:

- easier to understand
- more likely to inspire action
- easier to remember than isolated numbers

The source material also emphasized that stories can increase engagement compared with raw data alone.

### Parts Of A Good Data Story

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

### What Makes A Story Stick

Two reasons data stories work well:

- they create engagement
- they improve retention

People tend to remember stories more easily than isolated numbers. This does not mean you should replace evidence with emotion. It means you should package evidence in a form that human attention and memory can handle.

Warning: Emotion should support understanding and action, not distort the evidence. Clarity still comes first.

### Credibility And Trust

Good communication is not just about being noticed. It is also about being believed.

Credibility improves when you:

- keep visual conventions honest
- cite credible sources
- stay consistent in wording and design
- preserve a reputation for integrity over time
- bring in subject matter experts when interpretation needs domain authority

Trust is especially important in data storytelling because the audience is not only receiving information. They are deciding whether to accept the message and act on it.

#### Avoid Common Credibility Errors

- avoid truncating the y-axis on bar charts unless you clearly note it
- keep intervals consistent on axes, especially in line charts
- do not use clutter or decoration that makes interpretation harder
- do not use extra colors unless they carry meaning

### A Practical Workflow For Presenting Insights

When preparing a communication deliverable, this sequence works well:

1. identify the audience and desired decision
2. define the single main insight
3. choose the simplest visualization that supports that insight
4. add the business context needed to interpret it
5. write or present a short narrative around the implication
6. remove clutter and test whether the message is still clear
7. gather audience feedback and refine

### Common Failure Modes

- leading with charts before defining the message
- presenting too many insights at once
- using complex visuals to impress rather than clarify
- assuming the audience interprets a chart the same way you do
- forgetting to connect the result back to a business objective
- ignoring audience feedback when a visualization is confusing

### Quick Checklist

Before sharing an insight, check:

- Who is this for?
- What one thing should they remember?
- What action or decision should this support?
- Is the chart type appropriate for the data?
- Can I remove anything unnecessary?
- Have I added enough context for correct interpretation?

## Reports and Presentations

Reports and presentations are the delivery layer of data communication. After the question is framed and the insight is clarified, you still need to decide what to show, what to leave out, and which format best supports the audience's decision.

Key point: 好的分析不只要「說得懂」，還要「交付得對」。同一組分析結果，交給 technical colleague、manager、customer 的形式可能完全不同。

### Start With The Delivery Question

Before building a report, deck, or memo, clarify four things:

1. who is the audience
2. what is the purpose
3. what is the main message
4. what format best fits the situation

This is the practical planning layer that sits between insight generation and final communication.

### Use Personas To Guide Selection

Persona thinking helps decide what level of detail belongs in the deliverable.

Questions to ask:

- Is the audience technical, non-technical, or mixed?
- Are they making a strategic decision or handling an operational task?
- How much background do they already have?
- How much time do they have?
- Are they the decision maker, reviewer, or implementer?

Tip: Different personas should often get different findings, not just different wording.

### Select Findings, Not Everything

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

### Match The Format To The Goal

Different communication goals imply different formats.

| Purpose | Typical use | Best-fit format |
| --- | --- | --- |
| Informative | Share current status or findings | Summary report, dashboard review, short presentation |
| Instructional | Explain process or method | Technical report, workshop, walkthrough |
| Persuasive | Drive action or change | Executive memo, decision deck, recommendation presentation |

The choice of format should follow the decision context, not personal preference.

### Choose Between Written Reports And Presentations

Written reports and oral presentations solve different problems.

| Format | Best when | Main strength |
| --- | --- | --- |
| Written report | The reader may revisit details later | Precision, completeness, reproducibility |
| Presentation | The audience needs guided attention in real time | Focus, pacing, persuasion, interaction |

In many real settings, the two should support each other rather than compete:

- the report preserves detail
- the presentation drives attention to the key message

### Written Reports

A written report should be clear, precise, and reproducible.

Key qualities:

- readable by the intended audience
- explicit about context and findings
- structured enough to be scanned
- reproducible and properly sourced

#### Common Report Types

| Report type | Focus | Typical audience |
| --- | --- | --- |
| Summary report | Key findings and recommendations | Managers, executives, busy stakeholders |
| Final or analytical report | Full analysis, method, interpretation, evidence | Technical stakeholders, reviewers, project archive |
| Informational report | Status or descriptive information | Operational teams, monitoring use cases |

#### Summary Report Structure

A practical summary report can often be organized as:

1. contextual information
2. key findings
3. interpretation
4. recommendations or next steps

The point is not to reproduce the entire analysis. The point is to make the most important conclusions retrievable quickly.

#### Analytical Report Structure

An analytical or final report usually needs more depth:

1. problem and background
2. data and methods
3. analysis and results
4. interpretation
5. limitations
6. conclusions and recommendations
7. references or appendix

Tip: Many readers scan the introduction and conclusion first. Make sure those sections stand on their own.

### Reproducibility Belongs In Communication

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

### Executable Reports And Literate Analysis

Some reporting workflows go beyond static documents and combine narrative, code, figures, and metadata in one reproducible artifact.

Common examples include:

- R Markdown（實作見 [Reporting with R Markdown](../r-foundations/reporting-with-r-markdown.md)）
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

### Write Precisely And Clearly

Good reports reduce ambiguity.

Practical habits:

- prefer direct sentences over decorative phrasing
- define the point before expanding on it
- remove statements that add no information
- explain technical terms when the audience may not know them
- keep recommendations specific enough to act on

If a sentence cannot help the reader understand, decide, or verify, it probably does not belong.

### Plan Presentations Before Building Slides

Do not start with slides. Start with structure.

A simple planning frame:

- purpose
- audience
- message

This is often enough to prevent slide sprawl and unclear pacing.

### Presentation Types

Presentations often fall into three broad types:

- informative: explain what is happening
- instructional: explain how something works
- persuasive: argue for action or change

Knowing which one you are giving changes the content mix, tone, and call to action.

### Define The Central Message

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

### Presentation Structure

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

### Keep The Outline Tight

Aim for a small number of sections. The source material suggested five or fewer smaller parts, which is a good practical ceiling for many presentations.

A workable outline might be:

1. reason for the analysis
2. exploratory analysis
3. core model or method
4. conclusions
5. follow-up actions

### Build Better Slides

Slides should support the story, not replace it.

Useful heuristics:

- one message per slide
- keep slides short and dynamic
- judge slide quality by clarity, not by slide count
- use visuals to support the spoken narrative

Warning: Slide count and timing are weak quality metrics. A short deck can still be confusing, and a longer deck can still be coherent.

### Design Choices That Affect Readability

Color and layout choices influence comprehension directly.

Practical rules:

- use color to convey meaning, not decoration
- keep good contrast between text and background
- avoid relying on red and green combinations
- keep the palette limited, often no more than three main colors
- design for inclusive readability, including color-vision deficiencies

### Handling Time And Audience Size

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

### A Practical Delivery Workflow

Use this sequence when preparing a deliverable:

1. identify audience persona
2. define purpose and decision context
3. write the main message in one sentence
4. select only the findings that support that message
5. choose the right format
6. structure the report or presentation
7. add supporting visuals and evidence
8. verify clarity, credibility, and reproducibility

### Common Failure Modes

- mixing multiple problems into one deliverable
- choosing findings because they are interesting rather than relevant
- overloading non-technical audiences with technical detail
- hiding method details when technical review is required
- treating slide count as a quality metric
- writing reports that cannot be traced back to data and method

### Quick Checklist

Before sharing a report or presentation, ask:

- Who is this for?
- What decision should this support?
- What is the one-sentence message?
- Did I include only the findings needed for that message?
- Is the format appropriate?
- Is the result clear, precise, and reproducible?

## Related Notes

- 問題還模糊時，先讀 [Forming Analytical Questions](forming-analytical-questions.md)。
- 圖表機制與繪圖流程見 [Visualization](../data-manipulation-and-eda/visualization/README.md)；多圖組成決策畫面見 [Dashboard Design](dashboard-design.md)。
- 可重現報告的實作見 [Reporting with R Markdown](../r-foundations/reporting-with-r-markdown.md)（R Markdown / Quarto、參數化報告）。
