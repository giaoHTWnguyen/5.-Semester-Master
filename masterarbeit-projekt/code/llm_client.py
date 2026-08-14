import os, datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI
import json
from pathlib import Path

load_dotenv()

def ask_openai(prompt, system_prompt=None, model= 'gpt-5.6-luna',
               temperature=0.7, max_completion_tokens=1500):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})

    # gpt-5-modele akzeptieren nur temperature=1
    used_temp = 1.0 if model.startswith('gpt-5') else temperature 

    r = client.chat.completions.create(
        model = model,
        messages=messages,
        temperature=used_temp,
        max_completion_tokens=max_completion_tokens,
    )
    return {
        'answer': r.choices[0].message.content,
        'model_requested': model,
        'model_version': r.model,          # tatsächlich verwendeter Snapshot
        'input_tokens': r.usage.prompt_tokens,
        'output_tokens': r.usage.completion_tokens,
        'temperature': used_temp,
        'finish_reason': r.choices[0].finish_reason,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def ask_google(prompt, system_prompt, model='gemini-3.6-flash',
                temperature=1.0, max_tokens=2000):
    
    client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

    config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_prompt
            )

    r = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )

    # finish_reason aus dem ersten Candidate ziehen (Enum -> Name, z.B. "STOP", "MAX_TOKENS")
    finish_reason = None
    candidate = r.candidates[0] if r.candidates else None
    if candidate is not None and candidate.finish_reason is not None:
        fr = candidate.finish_reason
        finish_reason = fr.name if hasattr(fr, 'name') else str(fr)

    # answer defensiv lesen: bei abgeschnittener Antwort sind Textteile vorhanden,
    # bei blockierter oder leerer Antwort kann r.text fehlschlagen --> dann None
    if candidate is not None and candidate.content is not None and candidate.content.parts:
        answer = r.text
    else:
        answer = None

    return {
        'answer': r.text,
        'model_requested': model,
        'model_version': r.model_version,
        'input_tokens': r.usage_metadata.prompt_token_count,
        'output_tokens': r.usage_metadata.candidates_token_count,
        'temperature': temperature,
        'finish_reason': finish_reason,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
