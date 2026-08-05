from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / 'data'
KATALOGE = BASE / 'fragenkataloge'
ERGEBNISSE = BASE / 'results'
FIGURES = BASE.parent / 'thesis' / 'figures'

for p in (DATA, KATALOGE, ERGEBNISSE, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

MODELLE = {
    'openai': 'gpt-5.6-luna',
    'google': 'gemini-2.5-flash'
}

TEMPERATURE = 1 #default
MAX_TOKENS = 1500 

SYSTEM_PROMPT = "You are a data analyst answering questions about a dataset provided to you. Answer factually and precisely."

SYSTEM_PROMPT_EXP0 = "You are a data analyst answerung questions about exploratory data analysis. Answer factually and precisely."