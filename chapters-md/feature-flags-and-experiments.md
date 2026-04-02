# Feature Flags and Experiments

Claude Code's behavior isn't fixed at build time. A feature flag system allows Anthropic to control behavior remotely, rolling out new features gradually, running experiments, and adjusting settings without shipping new code.

## The Infrastructure

The feature flag system uses GrowthBook, an open-source feature flagging and experimentation platform. The integration uses SDK client key "sdk-zAZezfDKGoZuXXKe" and communicates with the GrowthBook API through the Anthropic API host at "https://api.anthropic.com/."

Remote evaluation is enabled, meaning flag values are computed on the server rather than locally. The cache uses two key attributes - an account identifier and an organization UUID - to ensure that flag values are consistent for a given user/organization combination. The initialization timeout is five seconds; if the GrowthBook service doesn't respond in time, the system falls back to defaults.

## The Flag Namespace

All Claude Code feature flags live under the "tengu_" namespace. There are approximately eight hundred and twenty-one flags in total, though most are minor variations or A/B test variants. The notable flags with known defaults include:

**Auto-mode and classifier flags:**
- "tengu_iron_gate_closed" (defaults to false): Controls whether the security classifier fails open or fails closed when it's unavailable. When false (the default), an unavailable classifier allows actions to proceed. When true, an unavailable classifier blocks all actions.
- "tengu_auto_mode_config": Configuration object for auto-mode behavior.
- "tengu_quiet_hollow" (defaults to false): Purpose relates to classifier behavior.

**Fast mode flags:**
- "tengu_penguins_off" (defaults to null): When null, fast mode is available. When set, fast mode is disabled.
- "tengu_marble_sandcastle" (defaults to false): Controls whether a native binary is required.

**Context and caching flags:**
- "tengu_system_prompt_global_cache" (defaults to false): Controls global caching of system prompts.
- "tengu_defer_all_bn4" (defaults to false): Controls bulk deferral of tool schemas.
- "tengu_defer_caveat_m9k" (defaults to false): Controls specific deferral caveats.
- "tengu_prompt_cache_1h_config" (defaults to null): Configuration for one-hour prompt caching.

**Cron flags:**
- "tengu_kairos_cron" (defaults to true): Enables the cron scheduling system.
- "tengu_kairos_cron_durable" (defaults to true): Enables durable persistence of scheduled jobs.

**Dream flags:**
- "tengu_onyx_plover" (defaults to null): Configures auto-dream behavior, including the minimum hours between dream cycles.

**Model access flags:**
- "tengu_coral_reef_sonnet" (defaults to null): Gates access to Sonnet 4.6 with one-million-token context.

**Miscellaneous flags:**
- "tengu_passport_quail" (defaults to false)
- "tengu_slate_thimble" (defaults to false)
- "tengu_herring_clock" (defaults to false)
- "tengu_amber_flint" (defaults to null)
- "tengu_amber_prism" (defaults to null)

The naming convention uses animal and object terms (plover, quail, herring, sandcastle) that serve as opaque codenames, making it difficult for external observers to infer a flag's purpose from its name alone.
