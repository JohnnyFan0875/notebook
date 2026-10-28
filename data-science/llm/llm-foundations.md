# LLM Foundations

LLM 在變成工具、agent 或產品之前的核心觀念：tokens、embeddings、context、訓練與 alignment、能力與限制；再往外一層看 generative AI 的模型家族（GAN、diffusion、transformer），最後是 chatbot 式互動（ChatGPT）的定位與限制。Transformer / attention 的內部機制見 [Transformers and Attention](../deep-learning/nlp-and-transformers/transformers-and-attention.md)。

Key point: 如果只學 prompt 與 API，很容易高估 LLM 「懂」多少。基礎觀念解釋了模型實際在做什麼、能力從哪裡來，以及為什麼它的失敗是可預期的。

## Large Language Models

Large language models are neural networks trained on large text corpora to predict and generate language.

Key point: An LLM does not "know" language the way a person does. It learns statistical patterns over tokens and uses those patterns to predict what text should come next in context.

### What Makes an LLM "Large"

The word "large" usually refers to both model scale and training scope.

| Dimension | Why It Matters |
| --- | --- |
| parameter count | more parameters can represent more complex patterns |
| training data volume | broader exposure improves general language behavior |
| compute budget | large-scale training enables more capable models |
| context handling | longer context windows allow richer input conditioning |

Tip: More parameters do not automatically mean a better application. System design still decides whether those capabilities become useful.

### How LLMs Differ from Earlier Language Models

Traditional language models and modern LLMs solve related problems, but at very different scales and flexibility levels.

| Earlier Language Models | Modern LLMs |
| --- | --- |
| narrower task scope | broader general-purpose behavior |
| weaker context handling | stronger use of surrounding context |
| limited adaptation | can be prompted, specialized, or fine-tuned |
| simpler statistical structure | transformer-based deep architectures |

Key point: The novelty of LLMs is not only that they generate text. It is that scale, context, and flexible prompting make one model usable across many tasks.

### Tokens, Embeddings, and Context

Before a model can process text, the text has to be represented numerically.

| Concept | Practical Meaning |
| --- | --- |
| Tokenization | split text into units the model can process |
| Embedding | map each token or text unit into a vector representation |
| Context | the surrounding sequence that shapes the next prediction |

A model does not see raw words directly. It sees token representations and relationships within a sequence.

Warning: Token-based processing means the model can be sensitive to phrasing, ordering, truncation, and context boundaries in ways that are not obvious to users.

### Why Context Matters

Language meaning depends on nearby language.

| Without Context | With Context |
| --- | --- |
| token meaning is ambiguous | the model can disambiguate intent |
| output stays generic | output becomes more task-specific |
| phrasing changes are fragile | prompt structure becomes more reliable |

This is one reason prompting, retrieval, and careful input construction matter so much in LLM systems.

### Why Transformers Matter

Modern LLMs are usually built on transformer architectures.

| Transformer Strength | Why It Helps |
| --- | --- |
| sequence-wide attention | relate each token to other relevant tokens |
| parallel processing | scale training more effectively than older sequential models |
| richer context modeling | capture longer-range relationships in text |
| flexible representation learning | support many downstream language tasks |

Tip: Attention、multi-head、positional encoding 等內部機制見 [Transformers and Attention](../deep-learning/nlp-and-transformers/transformers-and-attention.md)。這裡只需記得：transformer 是讓現代 LLM 能放大規模的架構。

### The Basic Training Story

At a high level, the model learns from token sequences by predicting text patterns.

1. collect large text datasets
2. tokenize the text
3. convert tokens into learned vector representations
4. train the model to predict tokens from context
5. adapt the model through instruction tuning, fine-tuning, or alignment methods

Key point: Pretraining gives broad language ability. Later stages shape that ability into something more useful, steerable, or domain-specific.

### Fine-Tuning and Alignment

Raw pretrained behavior is usually not enough for real use.

| Adaptation Step | Goal |
| --- | --- |
| fine-tuning | specialize the model for a domain or task |
| instruction tuning | make it follow user requests more reliably |
| RLHF or similar alignment methods | improve helpfulness, preference fit, or response quality |

This is the bridge from "predictive text engine" to "usable assistant."

### Unique Capabilities of LLMs

LLMs are impressive because one model can support many language tasks.

| Capability | Example |
| --- | --- |
| summarization | compress long notes into key points |
| rewriting | adjust tone, structure, or audience level |
| classification | label text by topic, sentiment, or intent |
| question answering | respond from context, retrieval, or instructions |
| generation | draft content, code, or explanations |

The practical lesson is not that the model is universally smart. It is that one general model can often be repurposed across many text workflows.

### Important Limits

LLMs are powerful, but they are not reliable by default.

| Limitation | Why It Happens |
| --- | --- |
| hallucination | fluent generation is not the same as grounded truth |
| context dependence | missing or weak context shifts output quality |
| sensitivity to prompt wording | small phrasing changes can alter behavior |
| weak guarantees | correctness, consistency, and safety are not automatic |

Tip: Many teams misread fluent language as strong understanding. In practice, an LLM often needs retrieval, tools, or guardrails to become dependable.

### Data, Cost, and Environmental Reality

Training and serving LLMs is resource-intensive.

| Concern | Why It Matters |
| --- | --- |
| large data needs | data sourcing and quality become strategic issues |
| compute cost | training and inference are expensive |
| environmental footprint | large-scale compute has energy and infrastructure impact |
| governance pressure | scale increases privacy, bias, and misuse concerns |

### Safety and Responsibility

The same flexibility that makes LLMs useful also creates risk.

| Risk | Example |
| --- | --- |
| deceptive or harmful content | persuasive misinformation or unsafe advice |
| manipulated prompts | hostile input can steer behavior away from intent |
| inappropriate outputs | unsafe, biased, or off-policy responses |
| unclear accountability | teams may not know who owns bad outcomes |

Key point: Responsibility does not begin after deployment. It begins when teams decide what data, objectives, safeguards, and review processes shape the model and its use.

### Where LLMs Fit

LLMs are best understood as a layer in a larger system.

1. the model provides language capability
2. prompting shapes the immediate task
3. retrieval or tools expand what the system can access
4. operations and evaluation keep the system reliable over time

If you want the system-design side next, continue with the main [LLM Applications and Systems](README.md) overview.

### Minimum Checklist

Before saying you understand what an LLM is, make sure you can explain:

1. why tokenization and embeddings matter
2. what transformers contribute beyond older language models
3. how pretraining differs from fine-tuning or alignment
4. why fluent output does not guarantee factual correctness
5. which risks come from scale, data, and open-ended generation

## Generative AI Overview

Generative AI refers to models that create new content rather than only classify, rank, or predict existing labels.

Key point: LLMs are one important branch of generative AI, but generative AI is broader. It includes systems that generate text, images, audio, code, video, and synthetic variations of existing data.

### What Makes Generative AI Different

Traditional predictive AI usually maps inputs to labels or scores. Generative AI produces new artifacts.

| Traditional AI | Generative AI |
| --- | --- |
| classify or predict | create or transform content |
| output is often a label or score | output can be text, image, audio, or code |
| narrower task framing | broader creative and assistive workflows |
| evaluation is often metric-driven | evaluation often includes quality, coherence, safety, and usefulness |

### Typical Generative Outputs

Generative systems can produce more than text.

| Output Type | Example |
| --- | --- |
| text | summarization, drafting, dialogue, code |
| image | illustration, concept art, design variation |
| audio | speech synthesis, music generation |
| multimodal output | systems that combine text with image or other media |

Tip: "Generative AI" is better understood as a family of content-producing models than as one single technology.

### Why It Expanded So Quickly

Several forces accelerated generative AI adoption.

| Driver | Why It Helped |
| --- | --- |
| larger datasets | models learned broader patterns |
| stronger compute | enabled larger model training |
| better architectures | transformers and diffusion models improved quality |
| product interfaces | chat, image tools, and APIs lowered adoption barriers |

### Foundation Models

Many generative products start from a general base model and adapt it later.

| Foundation Model Role | Why It Matters |
| --- | --- |
| broad pretraining | one model can support many downstream tasks |
| later customization | prompts, embeddings, or fine-tuning can specialize behavior |
| reuse across products | lowers the cost of building new applications |

Key point: Foundation models are powerful because they separate broad capability from task-specific adaptation.

### Major Model Families

Different generative tasks have historically leaned on different model families.

| Model Family | Often Used For | Main Idea |
| --- | --- | --- |
| transformers | text and multimodal reasoning | model long-range context effectively |
| GANs | image generation and synthesis | generator and discriminator improve each other adversarially |
| diffusion models | image generation and editing | learn to generate by reversing structured noise |

This is a simplification, but it is a useful orientation map.

### Why GANs Mattered

GANs were a major milestone in high-quality generation.

| GAN Strength | Practical Meaning |
| --- | --- |
| realistic outputs | generated artifacts can look convincing |
| strong image synthesis history | important in the evolution of visual generative AI |
| paired training dynamic | the generator improves by trying to fool a discriminator |

GANs are no longer the whole story, but they are part of why high-fidelity image generation became plausible.

### Why Diffusion Models Matter

Diffusion models became especially important for image generation.

| Diffusion Benefit | Why It Helps |
| --- | --- |
| high visual quality | strong results for image creation and editing |
| controllable generation | prompts and conditioning can steer outcomes |
| stable modern ecosystem | widely used in practical image-generation tools |

### Why Transformers Matter Beyond Text

Transformers mattered not only because they improved text generation, but because they improved context handling and coherence.

| Transformer Contribution | Why It Changed Generative AI |
| --- | --- |
| stronger context modeling | better long-range dependencies in text |
| scalable pretraining | enabled foundation-model workflows |
| flexible representation learning | supported transfer into many tasks |
| multimodal extension paths | helped bridge language with other media types |

### Evaluation Is Harder Than It Looks

Generative AI quality is harder to judge than simple classification accuracy.

| Evaluation Question | Why It Is Hard |
| --- | --- |
| Is the output coherent? | quality can be subjective |
| Is it useful? | usefulness depends on context and user goal |
| Is it safe? | harmful or deceptive output may still look polished |
| Is it original enough? | generated content can raise attribution and ownership concerns |

Warning: A polished output can still be wrong, unsafe, derivative, or legally problematic.

### Implementation Challenges

Generative systems are attractive, but difficult to operationalize cleanly.

| Challenge | Why It Shows Up |
| --- | --- |
| prompt sensitivity | outputs shift with wording and input structure |
| cost and latency | generation can be expensive or slow |
| evaluation ambiguity | quality cannot always be reduced to one metric |
| user misuse | open-ended systems invite adversarial or unsafe requests |

### Ethical and Legal Pressure

Generative AI introduces responsibility questions that teams cannot ignore.

| Concern | Example |
| --- | --- |
| bias and unfairness | outputs reinforce harmful stereotypes |
| privacy | prompts or training data may expose sensitive information |
| authorship and ownership | unclear rights over generated content |
| misuse | deceptive content, illegal help, or policy evasion |

Key point: Responsibility is not a separate afterthought. It is part of product, policy, and model design from the start.

### Prompt and Response Moderation

Open-ended generation requires active controls.

| Control Layer | Purpose |
| --- | --- |
| prompt moderation | block harmful or clearly disallowed requests |
| response moderation | detect unsafe generated output before release |
| policy design | define what the system should refuse or escalate |
| human review | handle ambiguous or high-risk cases |

Tip: Prompt moderation alone is not enough. Jailbreak-style inputs can still try to bypass simple safeguards.

### Boundaries of Generative AI

Generative AI is powerful, but it is not automatically the right tool.

It tends to fit best when:

1. content creation or transformation is central to the task
2. imperfect but useful drafts create real value
3. humans can review or guide high-stakes outputs

It fits less well when:

1. exact correctness is mandatory without review
2. the task is simple enough for deterministic software
3. governance or privacy requirements are incompatible with the data flow

### Relationship to LLMs

LLMs are one especially important subset of generative AI.

LLM 本身的基礎見本篇 [Large Language Models](#large-language-models) 一節。

### Minimum Checklist

Before saying you understand generative AI at a high level, make sure you can explain:

1. how generative AI differs from predictive AI
2. why foundation models matter
3. what roles transformers, GANs, and diffusion models each played
4. why evaluation and moderation are difficult
5. which legal, ethical, and misuse risks matter in real deployments

## Chatbot Interfaces (ChatGPT)

ChatGPT is a chatbot-style interface built on top of large language models so users can ask questions, give instructions, and iterate through multi-turn conversations.

Key point: ChatGPT feels conversational, but under the hood it is still a language model system responding to prompts and context. Its usefulness comes from general language flexibility, not from guaranteed truth or domain expertise.

### What Makes ChatGPT Different from Traditional Chatbots

Traditional chatbots often depend on fixed intents and predetermined replies. ChatGPT is more general.

| Traditional Chatbot | ChatGPT-Style System |
| --- | --- |
| predefined response patterns | more flexible language generation |
| limited question coverage | wider range of possible tasks |
| rigid menu-like flow | natural-language interaction |
| weaker adaptation to novel phrasing | better handling of varied wording |

Key point: ChatGPT is more generalizable because it interprets language patterns instead of only matching a narrow script.

### From Prompt to Response

At a high level, ChatGPT works like this:

1. the user provides a question or instruction
2. the model interprets the prompt in context
3. it generates a response token by token
4. the conversation state influences later turns

This is why prompt wording, prior messages, and topic drift all matter.

### Where ChatGPT Is Strong

ChatGPT is usually helpful when language transformation is the main job.

| Strength | Example |
| --- | --- |
| summarization | condense notes, articles, or meetings |
| drafting | generate first versions of emails, outlines, or reports |
| explanation | teach or restate concepts at different levels |
| brainstorming | generate options, themes, or approaches |
| rewriting | change tone, structure, or clarity |

Tip: A good mental model is "AI then human." Let the system produce a draft, then have a person review, refine, or reject it.

### ChatGPT Under the Hood

ChatGPT is an application layer over an LLM.

| Layer | Role |
| --- | --- |
| underlying language model | generates text based on learned patterns |
| conversation interface | manages turns and user interaction |
| prompt context | shapes what the model is trying to do |
| product rules | influence tone, guardrails, and behavior |

This is why ChatGPT is not identical to the raw model alone.

### Important Limitations

ChatGPT is useful, but it is not dependable in every setting.

| Limitation | Why It Matters |
| --- | --- |
| hallucination | it can generate plausible but false claims |
| bias | training data patterns can show up in outputs |
| context drift | long or mixed-topic conversations can degrade quality |
| limited private knowledge | it does not know personal facts unless provided |
| legal and ethical risk | outputs can raise ownership, safety, or compliance issues |

Warning: Confidence, fluency, and speed can make weak answers look stronger than they are.

### Conversation Quality Depends on Context

ChatGPT works better when the conversation stays well scoped.

| Helpful Practice | Why It Helps |
| --- | --- |
| keep one main topic per thread | reduces context confusion |
| provide useful background | improves relevance |
| remove irrelevant details | lowers distraction |
| ask for a clear output format | improves reuse |

Tip: If a conversation becomes messy, starting a fresh thread is often better than trying to rescue a badly mixed context window.

### Workflow Augmentation

ChatGPT is often best used to augment existing work instead of replacing judgment-heavy work entirely.

| Workflow Pattern | Why It Works |
| --- | --- |
| draft then review | keeps human control over final output |
| summarize then verify | speeds up reading while preserving checks |
| brainstorm then shortlist | uses the model for breadth, not final choice |
| explain then inspect | speeds learning without outsourcing truth completely |

Key point: Use ChatGPT where fast language generation adds leverage, not where unchecked correctness is mandatory.

### Identifying Good Use Cases

A task is a better fit for ChatGPT when:

1. language production or transformation is central
2. first-draft quality still creates value
3. a human can quickly evaluate the result

A task is a worse fit when:

1. the answer must be exact and auditable
2. the cost of an invented detail is high
3. sensitive or regulated data is involved carelessly

### Ownership and Privacy

Prompts and outputs can create real governance questions.

| Concern | Why It Matters |
| --- | --- |
| who owns the prompt | prompts may contain proprietary work or creative input |
| who owns the output | generated text may still require legal or policy review |
| prompt privacy | inputs can contain sensitive business or personal data |
| downstream reuse | copied outputs may be redistributed without proper checks |

Warning: Never assume a chat prompt is harmless just because it feels like a casual conversation.

### Ethics and Adoption

Wider access to ChatGPT democratizes AI use, but also increases misuse and inconsistency risk.

| Adoption Benefit | Adoption Risk |
| --- | --- |
| lower barrier to productivity | easier spread of low-quality or misleading output |
| broader experimentation | uneven safety and governance discipline |
| more accessible AI workflows | faster exposure of privacy or bias failures |

### Minimum Checklist

Before using ChatGPT in a real workflow, make sure you can explain:

1. how it differs from a traditional scripted chatbot
2. what kinds of tasks it is genuinely good at
3. which limitations matter for your use case
4. what human review step still exists
5. what ownership, privacy, or ethics issues apply to the prompt and output
