# Forschungsfragen:

1. Inwieweit basieren LLM-gestützte Ergebnisse der explorativen Datenanalyse auf den bereitgestellten Daten und nicht auf vortrainiertem Allgemeinwissen

2. In welchem Umfang stimmen die vom LLM generierten Analyseergebnissen mit den tatsächlich aus den Daten berechneten Kennzahlen und Zusammenhängen überein

3. Welchen Einfluss hat eine iterative Mensch-LLM-Interaktion auf die Konsistenz und Nachvollziehbarkeit der Analyseergebnisse

4. Wie viel Wissen haben LLMs über explorative Datenanalyse

# Durchführung

# Datensatz

## Erstellung Evaluationsframework:

Kategorie A: Faktische Korrektheit
→ Stimmt der genannte Mittelwert mit dem echten überein? (±5%?)

Kategorie B: Interpretationsqualität  
 → Wird ein Zusammenhang korrekt beschrieben?

Kategorie C: Halluzination
→ Behauptet das LLM etwas das nicht in den Daten ist?

## Test ständig wiederholen

- Dieselbe Frage 5-10mal stellen
- Verschiedene Prompt-Varianten Testen
- 2 verschiedene LLMs vergleichen (GPT-4o vs. Claude/Gemini/DeepSeek)

## Dokumentation

# Ergebnisse

# Interpretation

## Abgabetermin
