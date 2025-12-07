import os
def llm_response(prompt: str) -> str:
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        return "next_action:idle\nreply: (LLM not configured) I would ask for more details."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role':'system','content':'You are an orchestration agent.'},
                      {'role':'user','content': prompt}],
            max_tokens=200
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"next_action:idle\nreply: LLM error: {e}"
