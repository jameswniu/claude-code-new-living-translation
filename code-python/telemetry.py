"""
Claude Code telemetry and analytics configuration.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Telemetry Configuration
# ---------------------------------------------------------------------------

SERVICE_NAME = "claude-code"
LOGGER_NAME = "com.anthropic.claude_code.events"
VERSION = "2.1.87"
BUILD_TIME = "2026-03-29T01:39:21Z"

# Environment variables that control telemetry
DISABLE_TELEMETRY_VARS = [
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
    "DISABLE_TELEMETRY",
    "DISABLE_ERROR_REPORTING",
]


@dataclass
class TelemetryConfig:
    scheduled_delay_ms: int = 5000
    max_export_batch_size: int = 100
    max_queue_size: int = 1000
    skip_auth: bool = False
    base_url: Optional[str] = None
    path: Optional[str] = None


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled (all disable vars must be unset)."""
    import os
    return not any(
        os.environ.get(var, "").lower() in ("1", "true", "yes")
        for var in DISABLE_TELEMETRY_VARS
    )


# ---------------------------------------------------------------------------
# What Data Gets Sent to Anthropic
# ---------------------------------------------------------------------------

@dataclass
class SystemPromptTelemetry:
    """Sent on every API call as span attributes, and full content on first unique hash."""
    system_prompt_hash: str          # SHA hash of the full system prompt (including CLAUDE.md)
    system_prompt_preview: str       # First 500 chars
    system_prompt_length: int        # Total length
    system_prompt_full: Optional[str] = None  # Full content, sent ONCE per unique hash


@dataclass
class ClassifierMetrics:
    """Sent per tool call when auto-mode is active."""
    tool_name: str
    decision: str                    # "allowed", "blocked", "unavailable"
    classifier_model: Optional[str] = None
    classifier_duration_ms: Optional[int] = None
    classifier_input_tokens: Optional[int] = None
    classifier_output_tokens: Optional[int] = None
    classifier_cost_usd: Optional[float] = None
    consecutive_denials: int = 0
    total_denials: int = 0
    session_input_tokens: Optional[int] = None
    session_output_tokens: Optional[int] = None


@dataclass
class GrowthBookExperimentEvent:
    """Logged on every feature flag evaluation."""
    account_uuid: Optional[str] = None
    organization_uuid: Optional[str] = None
    session_id: Optional[str] = None
    user_attributes: Optional[dict] = None
    experiment_metadata: Optional[dict] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

API_ENDPOINTS = {
    "messages": "https://api.anthropic.com/v1/messages",
    "models": "https://api.anthropic.com/v1/models/claude-opus-4-6",
    "feedback": "https://api.anthropic.com/api/claude_cli_feedback",
    "metrics": "https://api.anthropic.com/api/claude_code/metrics",
    "org_metrics": "https://api.anthropic.com/api/claude_code/organizations/metrics_enabled",
    "transcripts": "https://api.anthropic.com/api/claude_code_shared_session_transcripts",
    "api_key": "https://api.anthropic.com/api/oauth/claude_cli/create_api_key",
    "roles": "https://api.anthropic.com/api/oauth/claude_cli/roles",
    "domain_info": "https://api.anthropic.com/api/web/domain_info",
    "mcp_registry": "https://api.anthropic.com/mcp-registry/v0/servers",
}

STAGING_ENDPOINTS = {
    "ant_dev": "https://beacon.claude-ai.staging.ant.dev",
    "anthropic": "https://api-staging.anthropic.com",
    "content": "https://staging.claudeusercontent.com",
    "fedstart": "https://claude-staging.fedstart.com",
}


# ---------------------------------------------------------------------------
# OAuth URLs
# ---------------------------------------------------------------------------

OAUTH_URLS = {
    "authorize_console": "https://platform.claude.com/oauth/authorize",
    "authorize_claude_ai": "https://claude.com/cai/oauth/authorize",
    "token": "https://platform.claude.com/v1/oauth/token",
    "callback": "https://platform.claude.com/oauth/code/callback",
    "client_metadata": "https://claude.ai/oauth/claude-code-client-metadata",
}
