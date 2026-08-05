import os, datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI

load_dotenv()

def ask_openai(prompt, system_prompt=None, modell= 'gpt-5.6-luna',
               temperature=1.0, max_completion_tokens=1500):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})

    # gpt-5-Modelle akzeptieren nur temperature=1
    used_temp = 1.0 if modell.startswith('gpt-5') else temperature 

    r = client.chat.completions.create(
        model = modell,
        messages=messages,
        temperature=used_temp,
        max_completion_tokens=max_completion_tokens,
    )
    return {
        'antwort': r.choices[0].message.content,
        'modell_angefragt': modell,
        'modell_version': r.model,          # tatsächlich verwendeter Snapshot
        'input_tokens': r.usage.prompt_tokens,
        'output_tokens': r.usage.completion_tokens,
        'temperature': used_temp,
        'finish_reason': r.choices[0].finish_reason,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def ask_google(prompt, system_prompt, modell='gemini-3.6-flash',
                temperature=1.0, max_tokens=2000):
    
    client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

    config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_prompt
            )

    r = client.models.generate_content(
        model=modell,
        contents=prompt,
        config=config,
    )
    return {
        'antwort': r.text,
        'modell_angefragt': modell,
        'modell_version': r.model_version,
        'input_tokens': r.usage_metadata.prompt_token_count,
        'output_tokens': r.usage_metadata.candidates_token_count,
        'temperature': temperature,
        'finish_reason': None,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def ask(provider, prompt, system_prompt=None, temperature=1.0, max_tokens=1500, modell=None):

    kwargs = {'modell' : modell} if modell else {}
    if provider == 'openai':
        return ask_openai(prompt, system_prompt=system_prompt, temperature=temperature, max_completion_tokens=max_tokens, **kwargs)
    elif provider == 'google':
        return ask_google(prompt, system_prompt=system_prompt, temperature=temperature, max_tokens=max_tokens, **kwargs)
    else:
        raise ValueError(f"Unbekannter Anbieter: {provider}")