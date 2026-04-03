# Claude Code: New Living Translation

Claude Code's intelligence architecture - Python implementation alongside accessible prose essays.

## What This Is

This repository contains two parallel representations of the "brain" of Anthropic's Claude Code CLI (version 2.1.87):

- **`code-python/`** - A Python implementation of the intelligence layer: the security classifier, permission system, model registry, system prompt, telemetry, and feature flags.
- **`chapters-md/`** - Accessible prose essays describing how the intelligence layer works. No code, just reader-friendly explanations.

If the production runtime is the body (the tools, the loop, the infrastructure), this is the mind (the decisions, the rules, the judgment calls).

## Legal Basis

This work constitutes commentary, analysis, and description of a publicly distributed software product. Descriptions of how software behaves - its decision rules, its safety policies, its pricing - are protected expression under the First Amendment.

The Supreme Court in Google v. Oracle (2021) held that reimplementation of functional interfaces constitutes fair use. This work goes further: it does not reimplement anything. It describes, in plain English, what a system does and why. This is the equivalent of a restaurant review describing the ingredients and techniques, not a stolen recipe.

### Relevant Case Law

- [Baker v. Selden, 101 U.S. 99 (1879)](https://supreme.justia.com/cases/federal/us/101/99/) - Ideas and methods of operation are not copyrightable; only the specific expression is protected.
- [Lotus Dev. Corp. v. Borland Int'l, Inc., 49 F.3d 807 (1st Cir. 1995), aff'd 516 U.S. 233 (1996)](https://law.justia.com/cases/federal/appellate-courts/F3/49/807/551122/) - Menu command hierarchies are uncopyrightable methods of operation under 17 U.S.C. Section 102(b).
- [Google LLC v. Oracle America, Inc., 593 U.S. 1 (2021)](https://supreme.justia.com/cases/federal/us/593/18-956/) - Reimplementation of functional API interfaces constitutes fair use; functional aspects of software are not entitled to the same copyright protection as creative works.
- [Sega Enterprises Ltd. v. Accolade, Inc., 977 F.2d 1510 (9th Cir. 1992)](https://law.justia.com/cases/federal/appellate-courts/F2/977/1510/305345/) - Reverse engineering of software for purposes of interoperability is fair use.
- [Sony Computer Entertainment v. Connectix Corp., 203 F.3d 596 (9th Cir. 2000)](https://law.justia.com/cases/federal/appellate-courts/F3/203/596/474793/) - Intermediate copying during reverse engineering to create a compatible product is fair use.

### First Amendment

- [Eldred v. Ashcroft, 537 U.S. 186 (2003)](https://supreme.justia.com/cases/federal/us/537/186/) - Copyright's built-in First Amendment accommodations include the idea/expression distinction and fair use.
- [17 U.S.C. Section 102(b)](https://www.law.cornell.edu/uscode/text/17/102) - "In no case does copyright protection for an original work of authorship extend to any idea, procedure, process, system, method of operation, concept, principle, or discovery."
- [17 U.S.C. Section 107 (Fair Use)](https://www.law.cornell.edu/uscode/text/17/107) - Fair use factors: purpose/character, nature of the work, amount used, and market effect.

### DMCA Context

- [Anthropic DMCA takedown (April 2026)](https://developers.slashdot.org/story/26/04/01/158240/anthropic-issues-copyright-takedown-requests-to-remove-8000-copies-of-claude-code-source-code) - Anthropic issued takedown requests targeting ~8,000 repositories containing copies of Claude Code source code. This repository contains no source code.

## How to Read This

Each essay covers one module of the intelligence layer. Start with "The Intelligence Layer" for the big picture, then read any essay that interests you. They are self-contained but cross-reference each other.

## Essays

- [The Intelligence Layer](chapters-md/the-intelligence-layer.md) - What "intelligence" means here
- [The Security Classifier](chapters-md/the-security-classifier.md) - The bouncer at the door
- [Context Compaction](chapters-md/context-compaction.md) - How conversations get summarized
- [The Dream System](chapters-md/the-dream-system.md) - Memory consolidation while you sleep
- [Feature Flags and Experiments](chapters-md/feature-flags-and-experiments.md) - The control panel
- [The Model Registry](chapters-md/the-model-registry.md) - Every model, every price, every limit
- [The Permission System](chapters-md/the-permission-system.md) - Who gets to do what
- [The System Prompt](chapters-md/the-system-prompt.md) - The instructions behind every conversation
- [What Gets Sent Home](chapters-md/what-gets-sent-home.md) - Telemetry and data collection
- [The Tool Inventory](chapters-md/the-tool-inventory.md) - Every tool the agent can use
