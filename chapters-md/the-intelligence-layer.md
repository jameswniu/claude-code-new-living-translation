# The Intelligence Layer

There's a useful way to think about Claude Code's architecture: the code is infrastructure, but the strings are the intelligence.

What does that mean? The code that runs the application - the loops, the structures, the network calls - is just plumbing. The actual intelligence of the system lives in its strings: the prompts that tell the model who it is, the rules that govern what's allowed, the thresholds that determine when to summarize, the pricing tables that track costs.

This collection of essays describes that intelligence layer. It's the decision-making core of Claude Code, version 2.1.87, as distributed through npm.

The intelligence layer consists of ten interconnected systems:

**The Security Classifier** watches every tool call in autonomous mode and decides whether to allow it or block it. It has thirty rules for things that should be blocked and seven exceptions for things that look dangerous but are actually fine.

**The Permission System** defines five modes of operation, from the cautious default (ask before doing anything risky) to full bypass mode (trust the agent completely). It maintains whitelists of commands that are always safe.

**The System Prompt** is the set of instructions injected at the start of every conversation. It tells the model who it is, how to behave, what to prioritize, and what to avoid.

**The Model Registry** catalogs every available model across four cloud providers, with pricing, context windows, and output limits for each.

**Context Compaction** kicks in when conversations grow too long. It summarizes the conversation into a structured format so the model can continue working without losing critical context.

**The Dream System** runs during idle periods to consolidate memories, resolve contradictions, and keep the agent's persistent knowledge organized.

**Feature Flags** control behavior through a GrowthBook integration, allowing Anthropic to enable, disable, or configure features remotely without shipping new code.

**Telemetry** tracks what data about your usage goes back to Anthropic - prompt hashes, token counts, classifier decisions, and experiment evaluations.

**The Tool Inventory** defines every tool available to the agent, from file operations to web searches to sub-agent spawning.

**Command Injection Detection** identifies attempts to smuggle malicious commands inside seemingly innocent tool calls.

Each of these is described in its own essay. Together, they form the intelligence that makes Claude Code behave the way it does - not the code that runs it, but the rules that guide it.
