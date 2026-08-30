from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderSpec:
    id: str
    label: str
    litellm_prefix: str
    default_model: str
    key_env_var: str
    needs_base_url: bool = False


PROVIDERS: list[ProviderSpec] = [
    ProviderSpec("openai", "OpenAI", "openai", "gpt-4o", "OPENAI_API_KEY"),
    ProviderSpec("anthropic", "Anthropic", "anthropic", "claude-sonnet-4-6", "ANTHROPIC_API_KEY"),
    ProviderSpec("groq", "Groq", "groq", "llama-3.3-70b-versatile", "GROQ_API_KEY"),
    ProviderSpec("gemini", "Google Gemini", "gemini", "gemini-2.0-flash", "GEMINI_API_KEY"),
    ProviderSpec("xai", "xAI Grok", "xai", "grok-2-latest", "XAI_API_KEY"),
    ProviderSpec("mistral", "Mistral", "mistral", "mistral-large-latest", "MISTRAL_API_KEY"),
    ProviderSpec("cohere", "Cohere", "cohere", "command-r-plus", "COHERE_API_KEY"),
    ProviderSpec("deepseek", "DeepSeek", "deepseek", "deepseek-chat", "DEEPSEEK_API_KEY"),
    ProviderSpec("nvidia", "Nvidia NIM", "nvidia_nim", "meta/llama3-70b-instruct", "NVIDIA_NIM_API_KEY"),
    ProviderSpec("openrouter", "OpenRouter", "openrouter", "openrouter/auto", "OPENROUTER_API_KEY"),
    ProviderSpec("together", "Together AI", "together_ai", "meta-llama/Llama-3-70b-chat-hf", "TOGETHER_API_KEY"),
    ProviderSpec("fireworks", "Fireworks AI", "fireworks_ai", "accounts/fireworks/models/llama-v3-70b-instruct", "FIREWORKS_API_KEY"),
    ProviderSpec("perplexity", "Perplexity", "perplexity", "sonar-pro", "PERPLEXITYAI_API_KEY"),
    ProviderSpec("cerebras", "Cerebras", "cerebras", "llama3.3-70b", "CEREBRAS_API_KEY"),
    ProviderSpec("anyscale", "Anyscale", "anyscale", "meta-llama/Meta-Llama-3-70B-Instruct", "ANYSCALE_API_KEY"),
    ProviderSpec("deepinfra", "DeepInfra", "deepinfra", "meta-llama/Meta-Llama-3-70B-Instruct", "DEEPINFRA_API_KEY"),
    ProviderSpec("azure_openai", "Azure OpenAI", "azure", "gpt-4o", "AZURE_API_KEY", needs_base_url=True),
    ProviderSpec("bedrock", "AWS Bedrock", "bedrock", "anthropic.claude-3-5-sonnet-20241022-v2:0", "AWS_ACCESS_KEY_ID"),
    ProviderSpec("vertex_ai", "Google Vertex AI", "vertex_ai", "gemini-1.5-pro", "VERTEXAI_API_KEY"),
    ProviderSpec("huggingface", "Hugging Face", "huggingface", "meta-llama/Meta-Llama-3-70B-Instruct", "HUGGINGFACE_API_KEY"),
    ProviderSpec("ollama", "Ollama Local", "ollama", "llama3.3", "OLLAMA_API_KEY", needs_base_url=True),
    ProviderSpec("opencode_zen", "OpenCode Zen", "openai", "opencode-zen-default", "OPENCODE_ZEN_API_KEY", needs_base_url=True),
]

PROVIDER_MAP = {p.id: p for p in PROVIDERS}


def get_provider(provider_id: str) -> ProviderSpec:
    if provider_id not in PROVIDER_MAP:
        raise ValueError(f"unknown provider {provider_id}")
    return PROVIDER_MAP[provider_id]


def litellm_model_string(provider_id: str, model_name: str) -> str:
    spec = get_provider(provider_id)
    if provider_id == "opencode_zen":
        return model_name
    return f"{spec.litellm_prefix}/{model_name}"


def provider_labels() -> list[tuple[str, str]]:
    return [(p.id, p.label) for p in PROVIDERS]
