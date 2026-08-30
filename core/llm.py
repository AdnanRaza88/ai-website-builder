import json
import litellm
from config.providers import litellm_model_string
from config.settings import settings


class LLMConfig:
    def __init__(self, provider_id: str, model_name: str, api_key: str, base_url: str | None):
        self.provider_id = provider_id
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def model_string(self) -> str:
        return litellm_model_string(self.provider_id, self.model_name)


def call_llm(config: LLMConfig, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
    kwargs = {
        "model": config.model_string(),
        "api_key": config.api_key,
        "temperature": settings.default_temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if config.base_url:
        kwargs["api_base"] = config.base_url
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = litellm.completion(**kwargs)
    return response["choices"][0]["message"]["content"]


def call_llm_json(config: LLMConfig, system_prompt: str, user_prompt: str) -> dict:
    raw = call_llm(config, system_prompt, user_prompt, json_mode=True)
    return json.loads(raw)
