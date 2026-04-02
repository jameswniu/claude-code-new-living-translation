# Context Compaction

Every AI model has a finite context window - the maximum amount of text it can consider at once. When a Claude Code conversation grows long enough to approach that limit, something has to give. That something is compaction: summarizing the conversation so far into a condensed form that preserves the essential information while freeing up space for new work.

## When Does Compaction Happen?

The system monitors the token count of the current conversation and compares it to the model's effective context window. Three thresholds determine the urgency:

**Warning level**: When the conversation reaches the effective window minus twenty thousand tokens, the system starts considering compaction. This is the "we should probably summarize soon" zone.

**Error level**: At the effective window minus thirteen thousand tokens, compaction becomes urgent. The system is running out of room.

**Blocking level**: At the effective window minus three thousand tokens, the system cannot proceed without compacting. There's simply no room left for the model to think and respond.

The system will attempt compaction up to three consecutive times. If all three attempts fail, it gives up - there's no point in an infinite retry loop.

## The Compaction Defaults

The compaction system has three default parameters: it requires a minimum of ten thousand tokens before it will bother compacting (summarizing a short conversation is wasteful), it needs at least five text-block messages, and it sets a maximum target of forty thousand tokens for the summary.

## What the Summary Looks Like

When compaction triggers, the model is given a detailed prompt asking it to create a thorough summary. The prompt asks for an analytical process first (wrapped in analysis tags), followed by a structured summary with nine sections:

**Primary Request and Intent** captures everything the user has explicitly asked for. This is critical because losing track of the user's original request during a long session would be a serious failure.

**Key Technical Concepts** lists the important technologies, frameworks, and patterns that have come up. This gives the model the vocabulary it needs to continue working.

**Files and Code Sections** enumerates the specific files that have been examined, modified, or created. Without this, the model would need to rediscover the project structure.

**Errors and Fixes** records what went wrong and how it was resolved. This prevents the model from repeating failed approaches.

**Problem Solving** documents the reasoning and troubleshooting process.

**All User Messages** lists every message from the user that is not a tool result. This ensures that the user's voice and preferences are preserved even when the raw messages are compressed away.

**Pending Tasks** outlines work that has been explicitly requested but not yet completed.

**Current Work** describes in precise detail what was being worked on immediately before compaction. This is perhaps the most important section - it's the "where was I?" that lets the model seamlessly resume.

**Optional Next Step** suggests what should happen next, providing continuity.

The prompt emphasizes thoroughness over brevity. It's better to have a slightly longer summary that preserves critical details than a concise one that loses important context. The goal is not to save tokens for their own sake but to make room for continued productive work.
