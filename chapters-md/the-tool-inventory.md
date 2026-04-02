# The Tool Inventory

Claude Code's power comes from its tools - thirty-eight distinct capabilities that let the agent interact with your system, the web, and other agents. Here's every tool, what it does, and how it fits into the bigger picture.

## File Operations

**Bash** executes shell commands and returns their output. The most powerful tool - it can do almost anything the user's shell can do. Commands are classified into safe categories (search, read, passthrough) and potentially dangerous categories (mutation). The default timeout is two minutes.

**Read** reads files from the filesystem with line numbers. Handles text files, images (displayed visually), PDFs (with page range support for large files), and Jupyter notebooks. Defaults to the first two thousand lines. Requires absolute paths.

**Write** creates or overwrites files. Requires that the file was read first if it already exists, to prevent accidental data loss. Creates parent directories automatically.

**Edit** performs precise string replacements in files. Requires the target string to be unique in the file (unless replacing all occurrences). Preferred over Write for modifications because it only shows what changed.

**Glob** finds files matching glob patterns (like "**/*.js"). Results sorted by modification time, limited to two hundred fifty matches.

**Grep** searches file contents using regular expressions, powered by ripgrep. Supports three output modes: file paths only, matching content lines, or match counts. Case-insensitive search available.

## Shell Execution

**PowerShell** executes PowerShell commands on Windows systems. The Windows counterpart to Bash.

## Sub-Agent Management

**Agent** launches autonomous sub-agents for complex tasks. Supports typed agents (Explore, Plan, general-purpose) with different tool access. Multiple agents can run in parallel.

**SendMessage** sends messages between agents in a team. The only way for teammates to communicate.

**SendUserMessage** sends a message visible to the user.

**TeamCreate** creates a multi-agent team with tmux-based coordination.

**TeamDelete** tears down a team and its agent processes.

## Task Tracking

**TaskCreate** creates a new trackable task with description and optional parent.

**TaskGet** retrieves a task by identifier.

**TaskList** lists all tasks in the session.

**TaskUpdate** changes a task's status.

**TaskOutput** gets a completed task's output.

**TaskStop** cancels a running task.

**TodoWrite** writes to a todo/task list (legacy tool).

## Planning

**EnterPlanMode** restricts the agent to read-only operations for strategic planning.

**ExitPlanMode** signals that planning is complete and ready for user approval.

## Web Access

**WebFetch** retrieves a URL, converts HTML to markdown, and processes it with AI. Includes a fifteen-minute cache.

**WebSearch** performs web searches and returns results.

## Scheduling

**CronCreate** schedules prompts for one-time or recurring execution.

**CronDelete** removes scheduled jobs.

**CronList** displays all scheduled jobs.

## Environment Isolation

**EnterWorktree** creates an isolated git worktree for safe experimentation.

**ExitWorktree** leaves a worktree (keeping or removing it).

**SandboxNetworkAccess** manages network access within the sandbox.

## Discovery

**ToolSearch** loads full schemas for deferred tools that aren't in the initial prompt. Supports exact selection, keyword search, and name-required search.

**ListMcpResourcesTool** lists resources from connected MCP servers.

**Skill** activates a bundled skill by expanding its specialized prompt.

## Development

**LSP** provides Language Server Protocol operations: go to definition, find references, hover, document symbols, workspace symbols, go to implementation, call hierarchy (prepare, incoming, outgoing).

**NotebookEdit** modifies Jupyter notebook cells.

**REPL** provides an interactive read-eval-print loop.

## Remote

**RemoteTrigger** manages scheduled remote agents through the claude.ai API. Supports listing, creating, updating, and running triggers at the endpoint "/v1/code/triggers/."

## Interaction

**AskUserQuestion** asks the user a question during execution, pausing for their response.

**Sleep** pauses execution for a specified duration.

## Built-In Agent Types

The Agent tool supports several pre-configured agent types:

**general-purpose**: Full tool access for complex multi-step tasks.

**Explore**: Optimized for codebase exploration. Has all tools except Agent, ExitPlanMode, Edit, Write, and NotebookEdit (it can look but not touch).

**Plan**: Designed for architectural planning. Same tool restrictions as Explore.

These agent types balance capability against safety - exploration agents can't accidentally modify files, and planning agents can't accidentally execute changes.
