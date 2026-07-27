from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / 'data'
KATALOGE = BASE / 'fragenkataloge'
ERGEBNISSE = BASE / 'results'
FIGURES = BASE.parent / 'thesis' / 'figures'

for p in (DATA, KATALOGE, ERGEBNISSE, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

MODELLE = {
    'openai': 'gpt-4o',
    'google': 'gemini-2.5-flash'
}

TEMPERATURE = 0.7 # offene Entscheidung / default
MAX_TOKENS = 2000 