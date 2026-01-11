from together import Together
import os

# Initialize Together client
# It will automatically read the TOGETHER_API_KEY from your environment
client = Together()

def query_llm(prompt: str, model: str = "arcee-ai/trinity-mini") -> str:
    """
    Send a prompt to Together.ai Qwen model and return the generated response.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[ERROR] Together.ai LLM request failed: {e}")
