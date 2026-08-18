import os, datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI
import json
from pathlib import Path
import time

load_dotenv()


# Retry mit Backoff um die API-AUfrufe, um bei TPM-Limit den Lauf nochmal zu starten

_RETRYABLE = {408, 409, 429, 500, 502, 503, 529}

def _status_code(e):
    for attr in ("status_code", "code", "http_status"):
        v = getattr(e, attr, None)
        if isinstance(v, int):
            return v
        return None

def _is_retryable(e):
    if _status_code(e) in _RETRYABLE:
        return True
    msg = str(e).lower()
    return any(s in msg for s in ("rate limit", "overloaded", "unavailable", "timeout", "429", "503"))

def _call_with_retry(fn, retries=6, base_delay=0.8, max_delay=60.0):
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as e:
            if attempt >= retries or not _is_retryable(e):
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"    retry in {delay:.0f}s ({str(e)[:100]})")
            time.sleep(delay)
            attempt += 1

# Reuse one client per provider instead of creating one per request

_openai_client = None
_google_client = None

def _get_openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    return _openai_client

def _get_google():
    global _google_client
    if _google_client is None:
        _google_client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])
    return _google_client


def ask_openai(prompt, system_prompt=None, model= 'gpt-5.6-luna',
               temperature=0.7, max_completion_tokens=1500, prompt_cache_key=None):
    client = _get_openai()
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})

    # gpt-5-modelle akzeptieren nur temperature=1
    used_temp = 1.0 if model.startswith('gpt-5') else temperature 

    extra = {}
    if prompt_cache_key:
        extra['prompt_cache_key'] = prompt_cache_key

    r = _call_with_retry(lambda: client.chat.completions.create(
        model = model,
        messages=messages,
        temperature=used_temp,
        max_completion_tokens=max_completion_tokens,
        **extra,
    ))

    usage = r.usage
    cached = 0
    details = getattr(usage, 'prompt_tokens_details', None)
    if details is not None:
        cached = getattr(details, 'cached_tokens', 0) or 0

    return {
        'answer': r.choices[0].message.content,
        'model_requested': model,
        'model_version': r.model,          # tatsächlich verwendeter Snapshot
        'input_tokens': r.usage.prompt_tokens,
        'cached_tokens': cached,
        'output_tokens': r.usage.completion_tokens,
        'temperature': used_temp,
        'finish_reason': r.choices[0].finish_reason,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
"""
Erstelle Kontext Caching um konstanten Datensatz und System Instructions zu halten. Alle späteren generate_content calls rufen diese Funktion auf um nur die Frage zu senden
Cached Content muss minimum token count exceeded (115k). Gibt den Cache Namen zurück
"""
def create_google_cache(data_block, system_prompt, model='gemini-3.6-flash', ttl_seconds=3600):
    client = _get_google()
    cache = client.caches.create(
        model=model,
        config=types.CreateCachedContentConfig(
            system_instruction=system_prompt,
            contents=[data_block],
            ttl=f'{ttl_seconds}s',
        ),
    )
    return cache.name

"""
Lösche Kontext Cache.
"""
def delete_google_cache(cache_name):
    if not cache_name:
        return
    try:
        _get_google().caches.delete(name=cache_name)
    except Exception:
        pass

"""
Einzige Gemini Generation
"""

def ask_google(prompt, system_prompt, model='gemini-3.6-flash',
                temperature=1.0, max_tokens=2000, cached_content=None):
    
    client = _get_google()

    cfg = dict(temperature=temperature, max_output_tokens=max_tokens)
    if cached_content:
        cfg['cached_content'] = cached_content
    else:
        cfg['system_instruction'] = system_prompt

    config = types.GenerateContentConfig(**cfg)

    r = _call_with_retry(lambda: client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    ))

    # finish_reason aus dem ersten Candidate ziehen (Enum -> Name, z.B. "STOP", "MAX_TOKENS")
    finish_reason = None
    candidate = r.candidates[0] if r.candidates else None
    if candidate is not None and candidate.finish_reason is not None:
        fr = candidate.finish_reason
        finish_reason = fr.name if hasattr(fr, 'name') else str(fr)

    # answer present only if the candidate has text parts
    has_text = (candidate is not None
                and candidate.content is not None
                and candidate.content.parts)

    um = r.usage_metadata
    cached = getattr(um, 'cached_content_token_count', 0) or 0   

    return {
        'answer': r.text if has_text else None,
        'model_requested': model,
        'model_version': r.model_version,
        'input_tokens': um.prompt_token_count,
        'cached_tokens': cached,
        'output_tokens': um.candidates_token_count,
        'temperature': temperature,
        'finish_reason': finish_reason,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
