# What Gets Sent Home

This essay describes what data Claude Code collects about your usage and where it goes. Understanding telemetry is important for making informed decisions about what you're comfortable with.

## The Service Identity

The telemetry system identifies itself with the service name "claude-code" and the logger name "com.anthropic.claude_code.events." The version at the time of this description is 2.1.87, built on March 29, 2026 at 01:39:21 UTC.

## How to Disable It

Three environment variables control telemetry:

Setting "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC" to "1", "true", or "yes" disables non-essential network traffic including telemetry.

Setting "DISABLE_TELEMETRY" to any truthy value disables telemetry specifically.

Setting "DISABLE_ERROR_REPORTING" to any truthy value disables error reporting.

If any of these variables is set to a truthy value, the system considers telemetry disabled.

## Telemetry Configuration

The telemetry pipeline batches events with a five-second scheduled delay, exports in batches of up to one hundred events, and queues up to one thousand events before dropping. Authentication can optionally be skipped, and the base URL and path can be configured.

## What Data Gets Sent

### System Prompt Telemetry

On every API call, the system sends span attributes about the system prompt:

A SHA hash of the full system prompt (including any CLAUDE.md content), a preview consisting of the first five hundred characters, and the total length. On the first call with a unique hash, the full system prompt text is also sent. This means Anthropic receives the complete system prompt - including your custom CLAUDE.md instructions - at least once per unique configuration.

### Classifier Metrics

When auto-mode is active, every tool call generates classifier metrics: the tool name, the decision (allowed, blocked, or unavailable), the classifier model used, how long classification took in milliseconds, the input and output tokens consumed by the classifier, the classifier's cost in USD, consecutive and total denial counts, and the session's cumulative input and output tokens.

### GrowthBook Experiment Events

Every feature flag evaluation logs an event containing the account UUID, organization UUID, session identifier, user attributes, and experiment metadata. This is how Anthropic tracks A/B test participation and outcomes.

## API Endpoints

Claude Code communicates with the following Anthropic endpoints:

- Messages API: "https://api.anthropic.com/v1/messages" (the main conversation endpoint)
- Models API: "https://api.anthropic.com/v1/models/claude-opus-4-6"
- Feedback: "https://api.anthropic.com/api/claude_cli_feedback"
- Metrics: "https://api.anthropic.com/api/claude_code/metrics"
- Organization metrics: "https://api.anthropic.com/api/claude_code/organizations/metrics_enabled"
- Shared transcripts: "https://api.anthropic.com/api/claude_code_shared_session_transcripts"
- API key creation: "https://api.anthropic.com/api/oauth/claude_cli/create_api_key"
- Roles: "https://api.anthropic.com/api/oauth/claude_cli/roles"
- Domain info: "https://api.anthropic.com/api/web/domain_info"
- MCP registry: "https://api.anthropic.com/mcp-registry/v0/servers"

## Staging Endpoints

For internal development, separate staging endpoints exist:

- Ant.dev beacon: "https://beacon.claude-ai.staging.ant.dev"
- Anthropic staging API: "https://api-staging.anthropic.com"
- Staging content: "https://staging.claudeusercontent.com"
- FedStart staging: "https://claude-staging.fedstart.com"

## OAuth URLs

Authentication uses these endpoints:

- Console authorization: "https://platform.claude.com/oauth/authorize"
- Claude.ai authorization: "https://claude.com/cai/oauth/authorize"
- Token exchange: "https://platform.claude.com/v1/oauth/token"
- Callback: "https://platform.claude.com/oauth/code/callback"
- Client metadata: "https://claude.ai/oauth/claude-code-client-metadata"

## The Takeaway

Claude Code sends telemetry about your usage patterns (token counts, costs, tool calls), your system prompt configuration (including custom instructions), and experiment participation. It does not send your conversation content through the telemetry pipeline (that goes through the Messages API as part of normal operation). You can disable the additional telemetry collection through environment variables, though the Messages API calls themselves are inherent to the product's function.
