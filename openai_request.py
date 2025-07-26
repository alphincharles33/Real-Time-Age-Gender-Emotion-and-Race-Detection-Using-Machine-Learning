from openai import OpenAI
import user_config

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = "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"
)
def send_request(query):
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response.choices[0].message.content
