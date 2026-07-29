import os, datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def ask_openai(prompt, modell= 'gpt-4o-mini', temperature=0.7, max_tokens=2000):
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

def ask_google(prompt, modell='gemini-3.6-flash', temperature=0.7, max_tokens=2000):
    
    client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
    r = client.models.generate_content(
        model=modell,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return {
        'antwort': r.text,
        'modell_angefragt': modell,
        'modell_version': r.model_version,
        'input_tokens': r.usage_metadata.prompt_token_count,
        'output_tokens': r.usage_metadata.candidates_token_count,
        'temperature': temperature,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

print(os.environ.get('GOOGLE_API_KEY', 'NICHT GEFUNDEN')[:7])

for name, fn, modell in [('OpenAI', ask_openai, 'gpt-4o mini'),
                         ('Google', ask_google, 'gemini-3.6-flash')]:
    print(f"=== {name} ===")
    try:
        r = fn("Antworte mit genau einem Wort: funktioniert.")
        print("antwort:", r['antwort'])
        print("version:", r['modell_version'])
        print("tokens:", r['input_tokens'], "/", r['output_tokens'])
    except Exception as e:
        print(f"Fehler: {e}")
    print()