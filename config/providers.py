from dataclasses import dataclass, field
import urllib.request
import json


@dataclass(frozen=True)
class ProviderSpec:
    id: str
    label: str
    litellm_prefix: str
    default_model: str
    key_env_var: str
    needs_base_url: bool = False
    known_models: tuple[str, ...] = field(default_factory=tuple)
    default_base_url: str = ""


PROVIDERS: list[ProviderSpec] = [
    ProviderSpec(
        "openai", "OpenAI", "openai", "gpt-4o", "OPENAI_API_KEY",
        known_models=("gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "o3-mini", "o4-mini"),
    ),
    ProviderSpec(
        "anthropic", "Anthropic", "anthropic", "claude-sonnet-4-6", "ANTHROPIC_API_KEY",
        known_models=("claude-sonnet-4-6", "claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5"),
    ),
    ProviderSpec(
        "groq", "Groq", "groq", "llama-3.3-70b-versatile", "GROQ_API_KEY",
        known_models=("llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"),
    ),
    ProviderSpec(
        "gemini", "Google Gemini", "gemini", "gemini-2.0-flash", "GEMINI_API_KEY",
        known_models=("gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-pro"),
    ),
    ProviderSpec(
        "xai", "xAI Grok", "xai", "grok-2-latest", "XAI_API_KEY",
        known_models=("grok-2-latest", "grok-3", "grok-3-mini", "grok-4"),
    ),
    ProviderSpec(
        "mistral", "Mistral", "mistral", "mistral-large-latest", "MISTRAL_API_KEY",
        known_models=("mistral-large-latest", "mistral-medium-latest", "mistral-small-latest", "codestral-latest"),
    ),
    ProviderSpec(
        "cohere", "Cohere", "cohere", "command-r-plus", "COHERE_API_KEY",
        known_models=("command-r-plus", "command-r", "command-a"),
    ),
    ProviderSpec(
        "deepseek", "DeepSeek", "deepseek", "deepseek-chat", "DEEPSEEK_API_KEY",
        known_models=("deepseek-chat", "deepseek-reasoner", "deepseek-coder"),
    ),
    ProviderSpec(
        "openrouter", "OpenRouter", "openrouter", "openrouter/auto", "OPENROUTER_API_KEY",
        known_models=("openrouter/auto", "anthropic/claude-sonnet-4", "openai/gpt-4o", "google/gemini-2.0-flash"),
    ),
    ProviderSpec(
        "together", "Together AI", "together_ai", "meta-llama/Llama-3.3-70B-Instruct-Turbo", "TOGETHER_API_KEY",
        known_models=("meta-llama/Llama-3.3-70B-Instruct-Turbo", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"),
    ),
    ProviderSpec(
        "fireworks", "Fireworks AI", "fireworks_ai", "accounts/fireworks/models/llama-v3p3-70b-instruct", "FIREWORKS_API_KEY",
        known_models=("accounts/fireworks/models/llama-v3p3-70b-instruct",),
    ),
    ProviderSpec(
        "perplexity", "Perplexity", "perplexity", "sonar-pro", "PERPLEXITYAI_API_KEY",
        known_models=("sonar-pro", "sonar", "sonar-reasoning"),
    ),
    ProviderSpec(
        "cerebras", "Cerebras", "cerebras", "llama3.3-70b", "CEREBRAS_API_KEY",
        known_models=("llama3.3-70b", "llama3.1-8b"),
    ),
    ProviderSpec(
        "azure_openai", "Azure OpenAI", "azure", "gpt-4o", "AZURE_API_KEY", needs_base_url=True,
        known_models=("gpt-4o", "gpt-4o-mini", "gpt-4.1"),
    ),
    ProviderSpec(
        "ollama", "Ollama Local", "ollama", "llama3.3", "OLLAMA_API_KEY", needs_base_url=True,
        known_models=("llama3.3", "llama3.2", "mistral", "qwen2.5", "codellama"),
        default_base_url="http://localhost:11434",
    ),
    ProviderSpec(
        "opencode_zen", "OpenCode Zen", "openai", "deepseek-v4-flash", "OPENCODE_ZEN_API_KEY", needs_base_url=True,
        known_models=(
            "deepseek-v4-flash",
            "deepseek-v4-flash-free",
            "deepseek-v4-pro",
            "big-pickle",
            "glm-4.7-free",
            "glm-4.6",
            "kimi-k2",
            "kimi-k2-thinking",
            "minimax-m2.7",
            "minimax-m2.5",
            "qwen3-coder",
            "grok-code",
        ),
        default_base_url="https://opencode.ai/zen/v1",
    ),
]

PROVIDER_MAP = {p.id: p for p in PROVIDERS}


def get_provider(provider_id: str) -> ProviderSpec:
    if provider_id not in PROVIDER_MAP:
        raise ValueError(f"unknown provider {provider_id}")
    return PROVIDER_MAP[provider_id]


def litellm_model_string(provider_id: str, model_name: str) -> str:
    spec = get_provider(provider_id)
    if provider_id == "opencode_zen":
        return f"openai/{model_name}"
    return f"{spec.litellm_prefix}/{model_name}"


def provider_labels() -> list[tuple[str, str]]:
    return [(p.id, p.label) for p in PROVIDERS]


def fetch_models_from_api(base_url: str, api_key: str) -> list[str]:
    if not base_url or not api_key:
        return []
    url = base_url.rstrip("/") + "/models"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []

    models: list[str] = []
    if isinstance(data, dict):
        items = data.get("data") or data.get("models") or []
        for item in items:
            if isinstance(item, dict):
                mid = item.get("id") or item.get("name") or item.get("model")
                if mid:
                    models.append(str(mid))
            elif isinstance(item, str):
                models.append(item)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                mid = item.get("id") or item.get("name")
                if mid:
                    models.append(str(mid))
            elif isinstance(item, str):
                models.append(item)
    return sorted(set(models))


def resolve_model_options(provider_id: str, api_key: str, base_url: str) -> tuple[list[str], str]:
    """Returns (model_ids, source_label). Tries live API first, then known list."""
    spec = get_provider(provider_id)
    effective_base = (base_url or spec.default_base_url or "").strip()

    if api_key and effective_base:
        live = fetch_models_from_api(effective_base, api_key)
        if live:
            return live, "fetched from API"

    if provider_id == "openai" and api_key:
        live = fetch_models_from_api("https://api.openai.com/v1", api_key)
        if live:
            return live, "fetched from API"

    if provider_id == "groq" and api_key:
        live = fetch_models_from_api("https://api.groq.com/openai/v1", api_key)
        if live:
            return live, "fetched from API"

    if provider_id == "openrouter" and api_key:
        live = fetch_models_from_api("https://openrouter.ai/api/v1", api_key)
        if live:
            return live, "fetched from API"

    known = list(spec.known_models) if spec.known_models else [spec.default_model]
    return known, "curated list"
