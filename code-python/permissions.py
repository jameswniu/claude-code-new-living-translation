"""
Claude Code permission modes, command whitelists, and dangerous patterns.

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional


# ---------------------------------------------------------------------------
# Permission Modes
# ---------------------------------------------------------------------------

class PermissionMode(Enum):
    DEFAULT = "default"
    ACCEPT_EDITS = "acceptEdits"
    BYPASS_PERMISSIONS = "bypassPermissions"
    DONT_ASK = "dontAsk"
    PLAN = "plan"


PERMISSION_MODES = [m.value for m in PermissionMode]


# ---------------------------------------------------------------------------
# Command Whitelists (bypass permission checks entirely)
# ---------------------------------------------------------------------------

# Search commands — auto-allowed, no permission check
SEARCH_COMMANDS = frozenset([
    "find", "grep", "rg", "ag", "ack", "locate", "which", "whereis",
])

# Read commands — auto-allowed, no permission check
READ_COMMANDS = frozenset([
    "cat", "head", "tail", "less", "more", "wc", "stat", "file",
    "strings", "ls", "tree", "du", "jq", "awk", "cut", "sort", "uniq", "tr",
])

# Passthrough / no-op commands
PASSTHROUGH_COMMANDS = frozenset(["echo", "printf", "true", "false", ":"])

# Filesystem mutation commands — need approval in default mode
MUTATION_COMMANDS = frozenset([
    "mv", "cp", "rm", "mkdir", "rmdir", "chmod", "chown", "chgrp",
    "touch", "ln", "cd", "export", "unset", "wait",
])

# Commands auto-allowed in acceptEdits mode (note: rm and sed are here!)
ACCEPT_EDITS_ALLOWED = frozenset(["mkdir", "touch", "rm", "rmdir", "mv", "cp", "sed"])

# Shell operators that split compound commands
SHELL_OPERATORS = frozenset(["&&", "||", ";", ";;", "|"])
REDIRECT_OPERATORS = frozenset([">&", ">", ">>"])


# ---------------------------------------------------------------------------
# Safe Tools (skip classifier entirely)
# ---------------------------------------------------------------------------

SAFE_YOLO_ALLOWLISTED_TOOLS = frozenset([
    # Read-only file operations
    "Read",
    # Search / read-only
    "Grep", "Glob", "LSP", "ToolSearch", "ListMcpResourcesTool", "ReadMcpResourceTool",
    # Task management (metadata only)
    "TodoWrite", "TaskCreate", "TaskGet", "TaskUpdate", "TaskList", "TaskStop", "TaskOutput",
    # Plan mode / UI
    "AskUserQuestion", "EnterPlanMode", "ExitPlanMode",
    # Swarm coordination
    "TeamCreate", "TeamDelete", "SendMessage",
    # Misc safe
    "Sleep",
])


def is_auto_mode_allowlisted(tool_name: str) -> bool:
    """Check if a tool completely skips the security classifier."""
    return tool_name in SAFE_YOLO_ALLOWLISTED_TOOLS


# ---------------------------------------------------------------------------
# Dangerous Patterns
# ---------------------------------------------------------------------------

GIT_INTERNAL_PATHS = frozenset(["HEAD", "objects/", "refs/", "hooks/", ".git/"])


def is_git_hook_planting(command: str) -> bool:
    """Detect writes to .git/ internal paths that could plant malicious hooks."""
    lower = command.lower()
    writes_git = any(p in lower for p in [".git/hooks", ".git/config", ".git/HEAD"])
    runs_git = "git " in lower or lower.startswith("git")
    return writes_git and runs_git


# ---------------------------------------------------------------------------
# Permission Decision
# ---------------------------------------------------------------------------

@dataclass
class PermissionDecision:
    behavior: Literal["allow", "deny", "ask", "passthrough"]
    message: str = ""
    reason: str = ""


def check_accept_edits_mode(command: str) -> PermissionDecision:
    """In acceptEdits mode, auto-allow certain commands."""
    base_cmd = command.strip().split()[0] if command.strip() else ""
    if base_cmd in ACCEPT_EDITS_ALLOWED:
        return PermissionDecision(
            behavior="allow",
            reason=f"mode:acceptEdits auto-allows {base_cmd}",
        )
    return PermissionDecision(behavior="passthrough", message=f"No mode-specific handling for '{base_cmd}'")


def check_permission_mode(command: str, mode: PermissionMode) -> PermissionDecision:
    """Check permission based on current mode."""
    if mode == PermissionMode.BYPASS_PERMISSIONS:
        return PermissionDecision(behavior="passthrough", message="Bypass mode handled in main flow")
    if mode == PermissionMode.DONT_ASK:
        return PermissionDecision(behavior="passthrough", message="DontAsk mode handled in main flow")
    if mode == PermissionMode.ACCEPT_EDITS:
        return check_accept_edits_mode(command)
    return PermissionDecision(behavior="passthrough", message="No mode-specific validation required")


def is_command_read_only(command: str) -> bool:
    """Check if a command is in the read-only whitelist."""
    base_cmd = command.strip().split()[0] if command.strip() else ""
    return base_cmd in SEARCH_COMMANDS or base_cmd in READ_COMMANDS
