# The Model Registry

Claude Code doesn't just talk to one model. It maintains a comprehensive registry of eleven model configurations, each available through four different cloud providers. This essay describes every model, its pricing, its capabilities, and the infrastructure that manages them.

## The Four Providers

Every model is available through four deployment paths:

**First-party (Anthropic direct)**: The standard API at api.anthropic.com. Model identifiers look like "claude-opus-4-6" or "claude-sonnet-4-5-20250929."

**Bedrock (AWS)**: Amazon's managed AI service. Model identifiers have the prefix "us.anthropic." followed by the model name and a version suffix, like "us.anthropic.claude-opus-4-6-v1."

**Vertex (Google Cloud)**: Google's AI platform. Model identifiers use an "@" symbol for versioning, like "claude-opus-4-6" or "claude-sonnet-4-5@20250929."

**Foundry**: Another deployment option with simplified model identifiers like "claude-opus-4-6" or "claude-sonnet-4-5."

## The Eleven Models

The registry includes models spanning several generations:

**Sonnet 3.5** (released October 2024): The first-party identifier is "claude-3-5-sonnet-20241022." A capable mid-tier model.

**Haiku 3.5** (released October 2024): The first-party identifier is "claude-3-5-haiku-20241022." The fast, affordable option.

**Sonnet 3.7** (released February 2025): The first-party identifier is "claude-3-7-sonnet-20250219." An improved mid-tier model.

**Sonnet 4.0** (released May 2025): The first-party identifier is "claude-sonnet-4-20250514."

**Opus 4.0** (released May 2025): The first-party identifier is "claude-opus-4-20250514." The first generation-4 flagship.

**Opus 4.1** (released August 2025): The first-party identifier is "claude-opus-4-1-20250805."

**Sonnet 4.5** (released September 2025): The first-party identifier is "claude-sonnet-4-5-20250929."

**Haiku 4.5** (released October 2025): The first-party identifier is "claude-haiku-4-5-20251001."

**Opus 4.5** (released November 2025): The first-party identifier is "claude-opus-4-5-20251101."

**Sonnet 4.6**: The first-party identifier is "claude-sonnet-4-6." The current default model for Claude Code.

**Opus 4.6**: The first-party identifier is "claude-opus-4-6." The most capable model available.

## Pricing

All prices are in US dollars per million tokens.

**Sonnet 4.6**: Three dollars for input tokens, fifteen dollars for output tokens, three dollars and seventy-five cents for prompt cache writes, and thirty cents for prompt cache reads. Web search requests cost one cent each.

**Opus 4.6**: Fifteen dollars for input tokens, seventy-five dollars for output tokens, eighteen dollars and seventy-five cents for prompt cache writes, and one dollar and fifty cents for prompt cache reads.

**Sonnet 4.5**: Five dollars input, twenty-five dollars output, six dollars and twenty-five cents cache write, fifty cents cache read.

**Opus 4.5**: Thirty dollars input, one hundred fifty dollars output, thirty-seven dollars and fifty cents cache write, three dollars cache read.

**Haiku 3.5**: Eighty cents input, four dollars output, one dollar cache write, eight cents cache read.

**Haiku 4.5**: One dollar input, five dollars output, one dollar and twenty-five cents cache write, ten cents cache read.

The older Sonnet models (3.5, 3.7, 4.0) share the same pricing tier as Sonnet 4.6. The older Opus models (4.0, 4.1) share pricing with Sonnet 4.5.

## Context Windows

The default context window for all models is two hundred thousand tokens. However, models in the 4.6 family (Opus 4.6 and Sonnet 4.6) can access a one-million-token context window if the user has been granted access through a feature flag.

## Output Token Limits

Each model has a default output limit and an upper limit:

Opus 4.6 defaults to sixty-four thousand output tokens, with an upper limit of one hundred and twenty-eight thousand.

Sonnet 4.6 defaults to thirty-two thousand, with the same one hundred and twenty-eight thousand upper limit.

Opus 4.5, Sonnet 4.x, and Haiku 4.x default to thirty-two thousand with a sixty-four thousand upper limit.

Opus 4.0 and 4.1 are capped at thirty-two thousand with no higher limit available.

The older 3.x models have lower limits: Sonnet 3.5 and Haiku 3.5 cap at eight thousand one hundred and ninety-two tokens, while Sonnet 3.7 defaults to thirty-two thousand with a sixty-four thousand limit.

## User-Facing Aliases

Users don't need to type full model identifiers. The system provides shortcuts: "sonnet" (current Sonnet), "opus" (current Opus), "haiku" (current Haiku), "best" (most capable model), "sonnet[1m]" and "opus[1m]" (with one-million-token context), and "opusplan" (Opus with planning mode).

## Display Names

When showing model names to users, the system uses friendly names: "Opus 4.6", "Sonnet 4.6", "Opus 4.5", "Sonnet 4.5", "Haiku 4.5", "Haiku 3.5", "Sonnet 4.0", "Sonnet 3.7", "Sonnet 3.5", "Opus 4.1", and "Opus 4.0."

## Cost Calculation

The cost of an API call is calculated by multiplying each token type's count by its per-million-token price: input tokens times the input price, output tokens times the output price, cache-read tokens times the cache-read price, and cache-write tokens times the cache-write price. The four products are summed to get the total cost.
