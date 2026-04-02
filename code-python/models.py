"""
Claude Code model registry, pricing, and context window configuration.

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class ModelProvider:
    first_party: str
    bedrock: str
    vertex: str
    foundry: str


@dataclass(frozen=True)
class ModelPricing:
    """Per-million-token pricing in USD."""
    input_tokens: float
    output_tokens: float
    prompt_cache_write_tokens: float
    prompt_cache_read_tokens: float
    web_search_requests: float = 0.01


@dataclass(frozen=True)
class ModelLimits:
    default_max_output: int
    upper_limit_max_output: int
    context_window: int  # 200_000 or 1_000_000


# ---------------------------------------------------------------------------
# Model Registry (11 models x 4 providers)
# ---------------------------------------------------------------------------

MODELS = {
    "sonnet37": ModelProvider(
        first_party="claude-3-7-sonnet-20250219",
        bedrock="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        vertex="claude-3-7-sonnet@20250219",
        foundry="claude-3-7-sonnet",
    ),
    "sonnet35": ModelProvider(
        first_party="claude-3-5-sonnet-20241022",
        bedrock="anthropic.claude-3-5-sonnet-20241022-v2:0",
        vertex="claude-3-5-sonnet-v2@20241022",
        foundry="claude-3-5-sonnet",
    ),
    "haiku35": ModelProvider(
        first_party="claude-3-5-haiku-20241022",
        bedrock="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        vertex="claude-3-5-haiku@20241022",
        foundry="claude-3-5-haiku",
    ),
    "haiku45": ModelProvider(
        first_party="claude-haiku-4-5-20251001",
        bedrock="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        vertex="claude-haiku-4-5@20251001",
        foundry="claude-haiku-4-5",
    ),
    "sonnet40": ModelProvider(
        first_party="claude-sonnet-4-20250514",
        bedrock="us.anthropic.claude-sonnet-4-20250514-v1:0",
        vertex="claude-sonnet-4@20250514",
        foundry="claude-sonnet-4",
    ),
    "sonnet45": ModelProvider(
        first_party="claude-sonnet-4-5-20250929",
        bedrock="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        vertex="claude-sonnet-4-5@20250929",
        foundry="claude-sonnet-4-5",
    ),
    "opus40": ModelProvider(
        first_party="claude-opus-4-20250514",
        bedrock="us.anthropic.claude-opus-4-20250514-v1:0",
        vertex="claude-opus-4@20250514",
        foundry="claude-opus-4",
    ),
    "opus41": ModelProvider(
        first_party="claude-opus-4-1-20250805",
        bedrock="us.anthropic.claude-opus-4-1-20250805-v1:0",
        vertex="claude-opus-4-1@20250805",
        foundry="claude-opus-4-1",
    ),
    "opus45": ModelProvider(
        first_party="claude-opus-4-5-20251101",
        bedrock="us.anthropic.claude-opus-4-5-20251101-v1:0",
        vertex="claude-opus-4-5@20251101",
        foundry="claude-opus-4-5",
    ),
    "opus46": ModelProvider(
        first_party="claude-opus-4-6",
        bedrock="us.anthropic.claude-opus-4-6-v1",
        vertex="claude-opus-4-6",
        foundry="claude-opus-4-6",
    ),
    "sonnet46": ModelProvider(
        first_party="claude-sonnet-4-6",
        bedrock="us.anthropic.claude-sonnet-4-6",
        vertex="claude-sonnet-4-6",
        foundry="claude-sonnet-4-6",
    ),
}

# ---------------------------------------------------------------------------
# Pricing Table (per million tokens)
# ---------------------------------------------------------------------------

PRICING: dict[str, ModelPricing] = {
    # Sonnet 4.6
    "claude-sonnet-4-6": ModelPricing(
        input_tokens=3,
        output_tokens=15,
        prompt_cache_write_tokens=3.75,
        prompt_cache_read_tokens=0.30,
    ),
    # Opus 4.6
    "claude-opus-4-6": ModelPricing(
        input_tokens=15,
        output_tokens=75,
        prompt_cache_write_tokens=18.75,
        prompt_cache_read_tokens=1.50,
    ),
    # Sonnet 4.5 / Sonnet 4.0 / Sonnet 3.7 / Sonnet 3.5
    "claude-sonnet-4-5-20250929": ModelPricing(
        input_tokens=5,
        output_tokens=25,
        prompt_cache_write_tokens=6.25,
        prompt_cache_read_tokens=0.50,
    ),
    # Opus 4.5
    "claude-opus-4-5-20251101": ModelPricing(
        input_tokens=30,
        output_tokens=150,
        prompt_cache_write_tokens=37.50,
        prompt_cache_read_tokens=3.00,
    ),
    # Haiku 3.5
    "claude-3-5-haiku-20241022": ModelPricing(
        input_tokens=0.80,
        output_tokens=4,
        prompt_cache_write_tokens=1.00,
        prompt_cache_read_tokens=0.08,
    ),
    # Haiku 4.5
    "claude-haiku-4-5-20251001": ModelPricing(
        input_tokens=1,
        output_tokens=5,
        prompt_cache_write_tokens=1.25,
        prompt_cache_read_tokens=0.10,
    ),
}

# Alias pricing for models that share the same tier
for _alias in [
    "claude-sonnet-4-20250514",
    "claude-3-7-sonnet-20250219",
    "claude-3-5-sonnet-20241022",
]:
    PRICING[_alias] = PRICING["claude-sonnet-4-6"]

for _alias in ["claude-opus-4-20250514", "claude-opus-4-1-20250805"]:
    PRICING[_alias] = PRICING["claude-sonnet-4-5-20250929"]


# ---------------------------------------------------------------------------
# Context Windows & Output Limits
# ---------------------------------------------------------------------------

DEFAULT_CONTEXT_WINDOW = 200_000


def get_context_window(model_id: str, *, has_1m_access: bool = False) -> int:
    """Get context window for a model. 1M requires feature flag access."""
    normalized = model_id.lower()
    if "opus-4-6" in normalized or "sonnet-4-6" in normalized:
        return 1_000_000 if has_1m_access else DEFAULT_CONTEXT_WINDOW
    return DEFAULT_CONTEXT_WINDOW


def get_max_output_tokens(model_id: str) -> tuple[int, int]:
    """Returns (default, upper_limit) output token counts."""
    normalized = model_id.lower()
    if "opus-4-6" in normalized:
        return 64_000, 128_000
    if "sonnet-4-6" in normalized:
        return 32_000, 128_000
    if any(x in normalized for x in ["opus-4-5", "sonnet-4", "haiku-4"]):
        return 32_000, 64_000
    if "opus-4-1" in normalized or "opus-4" in normalized:
        return 32_000, 32_000
    if "3-5-sonnet" in normalized or "3-5-haiku" in normalized:
        return 8_192, 8_192
    if "3-7-sonnet" in normalized:
        return 32_000, 64_000
    if "claude-3-opus" in normalized:
        return 4_096, 4_096
    if "claude-3-sonnet" in normalized:
        return 8_192, 8_192
    if "claude-3-haiku" in normalized:
        return 4_096, 4_096
    return 32_000, 64_000  # default


# ---------------------------------------------------------------------------
# Display Names
# ---------------------------------------------------------------------------

DISPLAY_NAMES: dict[str, str] = {
    "opus46": "Opus 4.6",
    "sonnet46": "Sonnet 4.6",
    "opus45": "Opus 4.5",
    "sonnet45": "Sonnet 4.5",
    "haiku45": "Haiku 4.5",
    "haiku35": "Haiku 3.5",
    "sonnet40": "Sonnet 4.0",
    "sonnet37": "Sonnet 3.7",
    "sonnet35": "Sonnet 3.5",
    "opus41": "Opus 4.1",
    "opus40": "Opus 4.0",
}


# ---------------------------------------------------------------------------
# Model Shortcuts (user-facing aliases)
# ---------------------------------------------------------------------------

MODEL_SHORTCUTS = ["sonnet", "opus", "haiku", "best", "sonnet[1m]", "opus[1m]", "opusplan"]


def calculate_cost(model_id: str, usage: dict) -> Optional[float]:
    """Calculate USD cost from token usage. Returns None if model not found."""
    pricing = PRICING.get(model_id)
    if pricing is None:
        return None
    input_cost = (usage.get("input_tokens", 0) / 1_000_000) * pricing.input_tokens
    output_cost = (usage.get("output_tokens", 0) / 1_000_000) * pricing.output_tokens
    cache_read_cost = (usage.get("cache_read_input_tokens", 0) / 1_000_000) * pricing.prompt_cache_read_tokens
    cache_write_cost = (usage.get("cache_creation_input_tokens", 0) / 1_000_000) * pricing.prompt_cache_write_tokens
    return input_cost + output_cost + cache_read_cost + cache_write_cost
