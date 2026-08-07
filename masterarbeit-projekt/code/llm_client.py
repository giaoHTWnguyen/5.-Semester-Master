import os, datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI
import json
from pathlib import Path

load_dotenv()

def ask_openai(prompt, system_prompt=None, model= 'gpt-5.6-luna',
               temperature=1.0, max_completion_tokens=1500):
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
        'antwort': r.choices[0].message.content,
        'model_angefragt': model,
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
    return {
        'antwort': r.text,
        'model_angefragt': model,
        'model_version': r.model_version,
        'input_tokens': r.usage_metadata.prompt_token_count,
        'output_tokens': r.usage_metadata.candidates_token_count,
        'temperature': temperature,
        'finish_reason': None,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def ask(provider, prompt, system_prompt=None, temperature=1.0, max_tokens=1500, model=None):

    kwargs = {'model' : model} if model else {}
    if provider == 'openai':
        return ask_openai(prompt, system_prompt=system_prompt, temperature=temperature, max_completion_tokens=max_tokens, **kwargs)
    elif provider == 'google':
        return ask_google(prompt, system_prompt=system_prompt, temperature=temperature, max_tokens=max_tokens, **kwargs)
    else:
        raise ValueError(f"Unbekannter Anbieter: {provider}")

"""
Baut den User Prompt aus einer Frage. Bei with_dataset=True wird der Datensatz vorangestellt. Das ist wichtig für das Caching: gleichbleibender Teil zuerst, wechselnde Frage zuletzt.
"""
def build_prompt(question_text, with_dataset=False, data_text=None):
    if with_dataset:
        if data_text is None:
            raise ValueError("with_dataset=True, but no data_text provided")
        return (
            "Here is a dataset in CSV format:\n\n"
            f"{data_text}\n\n"
            f"Question: {question_text}"
        )
    else:
        return question_text

"""
Hängt einen answer-entry als JSON-Zeile an die JSONL-Datei an. Schützt vor Datenverlust beim Absturz (sofortiges Schreiben)
"""
def save_answer(file, entry):
    file = Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

"""
Führt ein Experiment durch: jede Frage x jedes model x Wiederholungen.
Jede Antwort wird sofort gespeichert. Frischer Kontext pro Aufruf.
"""
def runner(experiment, questions, models, iterations, system_prompt, with_dataset=False, data_text=None, output_file=None):
    if output_file is None:
        output_file = Path('results') / f'{experiment}_answers.jsonl'

    total = len(questions) * len(models) * iterations
    count = 0

    for question in questions:
        user_prompt = build_prompt(question['question'],
                                   with_dataset=with_dataset,
                                   data_text=data_text)
        for provider, model in models:
            for iter in range(1, iterations + 1):
                count += 1
                try:
                    r = ask(provider, user_prompt, system_prompt=system_prompt, model=model)

                    entry = {
                        'experiment': experiment,
                        'question_id': question['id'],
                        'category': question.get('category'),
                        'iteration': iter,
                        'provider': provider,
                        'model': r['model_angefragt'],
                        'model_version': r['model_version'],
                        'prompt': user_prompt if not with_dataset else '[dataset + question]',
                        'answer': r['answer'],
                        'input_tokens': r['input_tokens'],
                        'output_tokens': r['output_tokens'],
                        'temperature': r['temperature'],
                        'finish_reason': r['finish_reason'],
                        'timestamp': r['timestamp'],
                    }
                    save_answer(output_file, entry)
                    status = 'ok'
                except Exception as e:
                    save_answer(output_file, {
                        'experiment': experiment,
                        'question_id': question['id'],
                        'iteration': iter,
                        'provider': provider,
                        'model': model,
                        'error': str(e),
                    })
                    status = f'ERROR: {e}'

                print(f"[{count}/{total}] {question['id']} {provider} Iter[iter]: {status}")
    print(f"\nFinished. {count} requests, saved in {output_file}")

"""
Lade den Fragenkatalog
"""    
def load_questions(experiment):
    path = Path('fragenkataloge') / f'{experiment}.json'
    with open(path, encoding='utf-8') as f:
        return json.load(f)