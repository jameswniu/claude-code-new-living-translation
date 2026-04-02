"""
Claude Code tool registry and descriptions.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolDefinition:
    name: str
    description: str
    search_hint: str = ""
    should_defer: bool = False
    max_result_size_chars: int = 100_000


# ---------------------------------------------------------------------------
# All 34+ Tools
# ---------------------------------------------------------------------------

TOOL_NAMES = {
    "Bash": "Bash",
    "Read": "Read",
    "Write": "Write",
    "Edit": "Edit",
    "Glob": "Glob",
    "Grep": "Grep",
    "Agent": "Agent",
    "WebFetch": "WebFetch",
    "WebSearch": "WebSearch",
    "Skill": "Skill",
    "ToolSearch": "ToolSearch",
    "PowerShell": "PowerShell",
    "NotebookEdit": "NotebookEdit",
    "TaskCreate": "TaskCreate",
    "TaskGet": "TaskGet",
    "TaskList": "TaskList",
    "TaskUpdate": "TaskUpdate",
    "TaskOutput": "TaskOutput",
    "TaskStop": "TaskStop",
    "AskUserQuestion": "AskUserQuestion",
    "EnterPlanMode": "EnterPlanMode",
    "ExitPlanMode": "ExitPlanMode",
    "SendMessage": "SendMessage",
    "SendUserMessage": "SendUserMessage",
    "TodoWrite": "TodoWrite",
    "Sleep": "Sleep",
    "REPL": "REPL",
    "LSP": "LSP",
    "RemoteTrigger": "RemoteTrigger",
    "EnterWorktree": "EnterWorktree",
    "ExitWorktree": "ExitWorktree",
    "ListMcpResourcesTool": "ListMcpResourcesTool",
    "SandboxNetworkAccess": "SandboxNetworkAccess",
    "TeamCreate": "TeamCreate",
    "TeamDelete": "TeamDelete",
    "CronCreate": "CronCreate",
    "CronDelete": "CronDelete",
    "CronList": "CronList",
}

# ---------------------------------------------------------------------------
# Tool Descriptions
# ---------------------------------------------------------------------------

BASH_DESCRIPTION = """Executes a given bash command and returns its output.

The working directory persists between commands, but shell state does not. The shell environment is initialized from the user's profile (bash or zsh).

IMPORTANT: Avoid using this tool to run find, grep, cat, head, tail, sed, awk, or echo commands, unless explicitly instructed. Instead, use the appropriate dedicated tool."""

READ_DESCRIPTION = """Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning of the file
- This tool can read images (PNG, JPG, etc), PDFs, and Jupyter notebooks
- Results are returned using cat -n format, with line numbers starting at 1"""

WRITE_DESCRIPTION = """Writes a file to the local filesystem.

Usage:
- This tool will overwrite the existing file if there is one at the provided path.
- You MUST use the Read tool first before writing to an existing file.
- Prefer the Edit tool for modifying existing files.
- NEVER create documentation files (*.md) or README files unless explicitly requested."""

EDIT_DESCRIPTION = """Performs exact string replacements in files.

Usage:
- You must use your Read tool at least once before editing.
- The edit will FAIL if old_string is not unique in the file.
- Use replace_all for replacing and renaming strings across the file."""

GREP_DESCRIPTION = """A powerful search tool built on ripgrep.

Usage:
- Supports full regex syntax (e.g., "log.*Error", "function\\s+\\w+")
- Filter files with glob parameter (e.g., "*.js", "**/*.py") or type parameter
- Output modes: "content" shows matching lines, "files_with_matches" shows only file paths"""

GLOB_DESCRIPTION = """Fast file pattern matching tool that works with any codebase size.
- Supports glob patterns like "**/*.js" or "**/*.py"
- Returns matching file paths sorted by modification time"""

AGENT_DESCRIPTION = """Launch a new agent to handle complex, multi-step tasks autonomously.

The Agent tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent type has specific capabilities and tools available to it.

Available agent types:
- general-purpose: All tools, multi-step tasks
- Explore: Fast codebase exploration (haiku model)
- Plan: Software architect for implementation plans
- statusline-setup: Configure status line (sonnet model)
- claude-code-guide: Documentation assistant"""

LSP_DESCRIPTION = """Interact with Language Server Protocol (LSP) servers to get code intelligence features.

Supported operations:
- goToDefinition: Find where a symbol is defined
- findReferences: Find all references to a symbol
- hover: Get hover information (documentation, type info)
- documentSymbol: Get all symbols in a document
- workspaceSymbol: Search for symbols across the workspace
- goToImplementation: Find implementations of an interface
- prepareCallHierarchy: Get call hierarchy item at a position
- incomingCalls: Find all callers of a function
- outgoingCalls: Find all callees of a function"""


# ---------------------------------------------------------------------------
# Agent Types
# ---------------------------------------------------------------------------

@dataclass
class AgentType:
    agent_type: str
    when_to_use: str
    model: str = "inherit"
    disallowed_tools: list[str] = None

    def __post_init__(self):
        if self.disallowed_tools is None:
            self.disallowed_tools = []


BUILT_IN_AGENTS = {
    "general-purpose": AgentType(
        agent_type="general-purpose",
        when_to_use="General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks.",
    ),
    "Explore": AgentType(
        agent_type="Explore",
        when_to_use="Fast agent specialized for exploring codebases. Use for finding files, searching code, or answering questions about the codebase.",
        model="haiku",
        disallowed_tools=["Agent", "ExitPlanMode", "Edit", "Write", "NotebookEdit"],
    ),
    "Plan": AgentType(
        agent_type="Plan",
        when_to_use="Software architect agent for designing implementation plans. Returns step-by-step plans, identifies critical files, and considers architectural trade-offs.",
        model="inherit",
        disallowed_tools=["Agent", "ExitPlanMode", "Edit", "Write", "NotebookEdit"],
    ),
    "statusline-setup": AgentType(
        agent_type="statusline-setup",
        when_to_use="Use this agent to configure the user's Claude Code status line setting.",
        model="sonnet",
    ),
    "claude-code-guide": AgentType(
        agent_type="claude-code-guide",
        when_to_use="Use this agent when the user asks questions about Claude Code features, hooks, slash commands, MCP servers, settings, IDE integrations.",
    ),
}
