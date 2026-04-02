# The Dream System

The name is evocative and intentional: just as human memory consolidation happens during sleep, Claude Code's memory consolidation happens during idle periods. The dream system is a reflective pass over the agent's memory files, synthesizing recent experiences into durable, well-organized memories.

## Why It Exists

Over the course of many sessions, an agent accumulates knowledge: who the user is, how they like to work, what projects are active, what mistakes have been made. Without consolidation, this knowledge becomes fragmented - scattered across session transcripts, duplicated in multiple places, or contradicted by newer information. The dream system acts as a cleanup and organization pass.

## The Four Phases

### Phase 1: Orient

The system starts by getting its bearings. It reads the memory directory to see what files already exist, reads the MEMORY.md index to understand the current organizational structure, and skims existing topic files so it can improve them rather than creating duplicates. If log directories or session subdirectories exist, it reviews recent entries there too.

This phase is about understanding the current state of memory before making changes. You don't reorganize a filing cabinet without first seeing what's in it.

### Phase 2: Gather Recent Signal

The system looks for new information worth persisting, using three sources in priority order:

First, daily logs (if they exist) - these are the append-only stream of what happened in each session, and they're the primary source of new signal.

Second, existing memories that have drifted - facts that contradict what the system now observes in the codebase. If a memory says "the project uses React 17" but the package.json now says React 18, that memory needs updating.

Third, session transcripts - but only through narrow, targeted searches. The system is explicitly told not to exhaustively read transcripts. They are large JSONL files, and reading them in full would be wasteful. Instead, the system greps for specific terms it already suspects are important.

### Phase 3: Consolidate

For each piece of information worth remembering, the system either creates a new memory file or updates an existing one. It follows the memory format conventions (YAML frontmatter with name, description, and type), and focuses on three priorities:

Merging new signal into existing topic files rather than creating near-duplicates. If there's already a file about the user's code review preferences, new observations about those preferences should be added to that file, not saved as a separate memory.

Converting relative dates to absolute dates. "Yesterday" becomes "2026-04-01" so the memory remains meaningful weeks or months later.

Deleting contradicted facts. If a recent investigation disproved something recorded in an old memory, the old memory is corrected at the source rather than leaving contradictory files.

### Phase 4: Prune and Index

The final phase cleans up the MEMORY.md index file, keeping it under two hundred lines and roughly twenty-five kilobytes. This index is an index, not a dump - each entry should be one line under about one hundred fifty characters, formatted as a link to the topic file with a brief description.

The system removes pointers to stale or superseded memories, demotes verbose entries (if an index line is over two hundred characters, it's carrying content that belongs in the topic file), adds pointers to newly important memories, and resolves any contradictions between files.

## When It Runs

The dream system is controlled by the feature flag "tengu_onyx_plover," which specifies the minimum hours between dream cycles. This prevents dreams from running too frequently (which would be wasteful) or too infrequently (which would allow memory drift to accumulate).

The system runs during idle periods - when the REPL is not actively processing user requests. This ensures that memory consolidation doesn't interfere with the user's work.
