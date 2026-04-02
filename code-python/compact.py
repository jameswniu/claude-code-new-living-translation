"""
Claude Code context compaction system.

"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Auto-Compact Thresholds
# ---------------------------------------------------------------------------

COMPACT_DEFAULTS = {
    "min_tokens": 10_000,
    "min_text_block_messages": 5,
    "max_tokens": 40_000,
}

# Threshold offsets from effective context window
WARNING_THRESHOLD_OFFSET = 20_000    # effectiveWindow - 20K
ERROR_THRESHOLD_OFFSET = 13_000      # effectiveWindow - 13K
BLOCKING_LIMIT_OFFSET = 3_000        # effectiveWindow - 3K


@dataclass
class CompactState:
    compacted: bool = False
    turn_id: str = ""
    turn_counter: int = 0
    consecutive_failures: int = 0


def get_auto_compact_threshold(effective_window: int) -> int:
    return effective_window - WARNING_THRESHOLD_OFFSET


def should_auto_compact(token_count: int, effective_window: int) -> bool:
    threshold = get_auto_compact_threshold(effective_window)
    return token_count >= threshold


# ---------------------------------------------------------------------------
# Compaction Prompt (9-section summary format)
# ---------------------------------------------------------------------------

COMPACTION_PROMPT = """Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions.
This summary should be thorough in capturing technical details, code patterns, and architectural decisions that would be essential for continuing development work without losing context.

Before providing your final summary, wrap your analysis in <analysis> tags to organize your thoughts and ensure you've covered all necessary points. In your analysis process:

1. Chronologically analyze each message and section of the conversation. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests
   - Key decisions, technical concepts and code patterns
   - Specific details like: file names, full code snippets, function signatures, file edits
   - Errors that you ran into and how you fixed them
   - Pay special attention to specific user feedback
2. Double-check for technical accuracy and completeness.

Your summary should include the following sections:

1. Primary Request and Intent: Capture all of the user's explicit requests and intents in detail
2. Key Technical Concepts: List all important technical concepts, technologies, and frameworks discussed.
3. Files and Code Sections: Enumerate specific files and code sections examined, modified, or created.
4. Errors and fixes: List all errors that you ran into, and how you fixed them.
5. Problem Solving: Document problems solved and any ongoing troubleshooting efforts.
6. All user messages: List ALL user messages that are not tool results.
7. Pending Tasks: Outline any pending tasks that you have explicitly been asked to work on.
8. Current Work: Describe in detail precisely what was being worked on immediately before this summary request.
9. Optional Next Step: List the next step that is related to the most recent work."""
