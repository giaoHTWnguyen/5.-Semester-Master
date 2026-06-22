# HowReliable are LLMs as Knowledge Bases? Re-thinking Facutality and Consistency

## Was findet man zum THema Zuverlässigkeit

Es gibt Zwei Säulen der Zuverlässigkeit

Faktualität (S.2): "Ein zuverlässiges Modell muss korrekte Antworten auf gelerntes Wissen (seen knowledge) geben und gleichzeitig vermeiden, falsche Behauptungen über ihm unbekanntes Wissen (unseen knowledge) aufzustellen. Für unbekanntes Wissen wird eine hohe "Uninformative Rate" z.B. die Antwort unsicher erwartet" S.1, 3

- bei bekanntem Wissen: hohe Korrektheit, niedrige Fehlerrate
- bei unbekanntem Wissen:

Konsistenz (S.2-3): Beschreibt die Fähigkeit eines Modells auf dieselbe Wissensfrage über mehrere Iterationen hinweg stabile und identische Antworten zu liefern. Ein ideales MOdell sollte bei korrekten Antworten konsistent und bei falschen Antworten eher inkonsistent sein. S.3

--> Korrekte Antworten sollen stabil bleiben, falsche Antworten sollen inkonsistent sein. Problematisch: größere Modelle sind auch bei falschen Antworten konsistent.: Siehe Experiment 1, Wiederholungen messen genau das

Reliability:

- folgende Kriterien müssen getroffen werden:
- 1. Kriterium: für gelerntes Wissen sollte LLM eine high rate für Konsistenz und korrekte Responses haben und eine low rate mit konsistenten falschen antworten
- 2. Kriterium: für unseen knowledge, muss die LLM eine high rate of uninformative oder inconsistent responses haben

Wichtiger Befund Modellgröße (S.7) Größere Modelle sind faktische bei bekanntem Wissen, aber konsistenter auch bei falschen Antworten. --> GPT-4o ist groß, also ist das Risiko auch hoch

WIchtiger Befund Prompting (S.7): "Unsure shots" im Prompt verbessern den Umgang mit unbekanntem Wissen erheblich. Relevant für mich: Begründung warum Prompt-Design in meiner Arbeit wichtig ist

## neue Metriken zur Messung

Zur Quantifizierung der Zuverl
