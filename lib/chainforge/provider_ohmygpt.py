from chainforge.providers import provider
from openai import OpenAI

client = OpenAI(
    base_url="https://api.ohmygpt.com/v1/",
    api_key="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"
)

# JSON schemas to pass react-jsonschema-form, one for this provider's settings and one to describe the settings UI.
OHMYGPT_SETTINGS_SCHEMA = {
  "settings": {
    "temperature": {
      "type": "number",
      "title": "temperature",
      "description": "Controls the 'creativity' or randomness of the response.",
      "default": 0,
      "minimum": 0,
      "maximum": 5.0,
      "multipleOf": 0.01,
    },
    "max_tokens": {
      "type": "integer",
      "title": "max_tokens",
      "description": "Maximum number of tokens to generate in the response.",
      "default": 2048,
      "minimum": 1,
      "maximum": 4096,
    },
  },
  "ui": {
    "temperature": {
      "ui:help": "Defaults to 0.",
      "ui:widget": "range"
    },
    "max_tokens": {
      "ui:help": "Defaults to 2048.",
      "ui:widget": "range"
    },
  }
}

@provider(name="OhMyGPT",
          emoji="🖇", 
          models=['gpt-3.5-turbo-0613', 'gpt-4-0613'],
          settings_schema=OHMYGPT_SETTINGS_SCHEMA)
def OhMyGPTCompletion(prompt: str, model: str, temperature: float = 0, **kwargs) -> str:
    print(f"Calling OhMyGPT model {model} with prompt '{prompt}'...")
    messages=[{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(model=model, messages=messages, temperature=temperature, **kwargs)
    return completion.choices[0].message.content