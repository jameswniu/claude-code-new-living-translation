"""
GrowthBook feature flag configuration.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


# ---------------------------------------------------------------------------
# GrowthBook Configuration
# ---------------------------------------------------------------------------

GROWTHBOOK_SDK_CLIENT_KEY = "sdk-zAZezfDKGoZuXXKe"
GROWTHBOOK_API_HOST = "https://api.anthropic.com/"
GROWTHBOOK_REMOTE_EVAL = True
GROWTHBOOK_CACHE_KEY_ATTRIBUTES = ["id", "organizationUUID"]
GROWTHBOOK_INIT_TIMEOUT_MS = 5000


@dataclass
class GrowthBookConfig:
    api_host: str = GROWTHBOOK_API_HOST
    client_key: str = GROWTHBOOK_SDK_CLIENT_KEY
    remote_eval: bool = GROWTHBOOK_REMOTE_EVAL
    cache_key_attributes: list[str] = None

    def __post_init__(self):
        if self.cache_key_attributes is None:
            self.cache_key_attributes = list(GROWTHBOOK_CACHE_KEY_ATTRIBUTES)


# ---------------------------------------------------------------------------
# Feature Flags (tengu_* namespace, 821 total)
# These are the flag NAMES — values come from GrowthBook server at runtime
# ---------------------------------------------------------------------------

# Key feature flags with known defaults from observed defaults
NOTABLE_FLAGS: dict[str, Any] = {
    # Auto-mode / classifier
    "tengu_iron_gate_closed": False,  # fail-open vs fail-closed when classifier unavailable
    "tengu_auto_mode_config": {},
    "tengu_quiet_hollow": False,

    # Fast mode
    "tengu_penguins_off": None,  # None = fast mode available
    "tengu_marble_sandcastle": False,  # native binary requirement

    # Context / caching
    "tengu_system_prompt_global_cache": False,
    "tengu_defer_all_bn4": False,
    "tengu_defer_caveat_m9k": False,
    "tengu_prompt_cache_1h_config": None,

    # Cron
    "tengu_kairos_cron": True,
    "tengu_kairos_cron_durable": True,

    # Dream
    "tengu_onyx_plover": None,  # auto-dream config (minHours)

    # Misc
    "tengu_passport_quail": False,
    "tengu_slate_thimble": False,
    "tengu_herring_clock": False,
    "tengu_amber_flint": None,
    "tengu_amber_prism": None,
    "tengu_coral_reef_sonnet": None,  # sonnet 4.6 1M context gate
}


def get_feature_flag(name: str, default: Any = None) -> Any:
    """
    Read a feature flag value. In production this calls GrowthBook SDK.
    Here we return the known default from observed defaults.
    """
    return NOTABLE_FLAGS.get(name, default)
