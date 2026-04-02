# The Permission System

Imagine giving someone the keys to your computer. How much do you trust them? The permission system is Claude Code's answer to that question, providing a spectrum from "ask me about everything" to "do whatever you want."

## Five Modes

The system defines five distinct permission modes:

**Default mode** is the cautious starting point. The agent asks for permission before performing any action that could modify the system. Read operations are free, but writes, shell commands, and network access require approval.

**Accept Edits mode** is a step up in trust. In addition to everything allowed in default mode, the agent can perform a specific set of filesystem mutations without asking: creating directories, creating files, deleting files and directories, moving files, copying files, and running sed (the stream editor). These are the bread-and-butter operations of code editing, and requiring approval for each one would make the agent painfully slow for development work.

**Bypass Permissions mode** is full trust. The agent can do anything without asking. This is for users who are comfortable with autonomous operation and want maximum speed.

**Don't Ask mode** is similar to bypass but with a different interaction model - the agent proceeds without prompting rather than requiring explicit mode selection.

**Plan mode** is the most restrictive. The agent can only read and search - no edits, no commands, no modifications of any kind. This is used when the agent is in planning mode, designing an approach before executing it.

## Command Whitelists

Regardless of the permission mode, certain commands are always allowed because they cannot modify the system:

**Search commands** are always allowed: find, grep, ripgrep, ag (silver searcher), ack, locate, which, and whereis. These only read the filesystem.

**Read commands** are always allowed: cat, head, tail, less, more, wc, stat, file, strings, ls, tree, du, jq, awk, cut, sort, uniq, and tr. These display or transform data without modifying anything.

**Passthrough commands** are always allowed because they're essentially no-ops: echo, printf, true, false, and the colon (shell no-op).

**Mutation commands** require approval in default mode: mv, cp, rm, mkdir, rmdir, chmod, chown, chgrp, touch, ln, cd, export, unset, and wait.

The system also recognizes **shell operators** that combine commands (&&, ||, semicolons, pipes) and **redirect operators** (>, >>, >&) which can change the effect of otherwise-safe commands.

## Safe Tools (Classifier Bypass)

Some tools completely skip the security classifier because they are inherently safe:

Read (file reading), Grep, Glob, LSP, ToolSearch, ListMcpResourcesTool, ReadMcpResourceTool (all read-only search and discovery tools).

TodoWrite, TaskCreate, TaskGet, TaskUpdate, TaskList, TaskStop, TaskOutput (all task management tools - they only modify metadata, not the system).

AskUserQuestion, EnterPlanMode, ExitPlanMode (interaction and planning tools).

TeamCreate, TeamDelete, SendMessage (swarm coordination tools).

Sleep (just pauses execution).

These tools are allowlisted because their effects are either invisible to the system (metadata only), require user interaction (questions), or are strictly read-only (search tools).

## Dangerous Patterns

The system watches for specific dangerous patterns, particularly writes to git internal paths. If a command attempts to write to ".git/hooks", ".git/config", or ".git/HEAD", it's flagged as a potential attempt to plant malicious git hooks. This detection checks whether the command both writes to a git internal path and runs a git command, which would be a classic hook-planting attack vector.

## Permission Decisions

When a command needs evaluation, the system produces a decision with one of four behaviors:

**Allow**: The command can proceed immediately.
**Deny**: The command is blocked.
**Ask**: The user should be prompted for approval.
**Passthrough**: No mode-specific handling applies; continue to the next check.

In accept-edits mode, the decision logic checks whether the base command (the first word of the command string) is in the accept-edits-allowed set. If it is, the command is allowed with a note explaining why. If not, the decision passes through to the default handling.
