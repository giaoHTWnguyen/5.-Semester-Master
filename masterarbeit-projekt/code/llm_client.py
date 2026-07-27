import os, datetime
from dotenv import load_dotenv

load_dotenv()

def ask_openai(prompt, modell= 'gpt-4o', temperature=0.7, max_tokens=2000):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    r = client.chat.completions.create(
        model = modell,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return {
        'antwort': r.choices[0].message.content,
        'modell_angefragt': modell,
        'modell_version': r.model,          # tatsächlich verwendeter Snapshot
        'input_tokens': r.usage.prompt_tokens,
        'output_tokens': r.usage.completion_tokens,
        'temperature': temperature,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


print(os.environ.get('OPENAI_API_KEY', 'NICHT GEFUNDEN')[:7])