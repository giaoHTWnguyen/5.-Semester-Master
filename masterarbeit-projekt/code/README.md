# Datenkonsistenz und Zuverlässigkeit in der LLM-gestützten explorativen Analyse

Code und Daten zur Masterarbeit im Studiengang Wirtschaftsinformatik an der HTW Berlin zum Sommersemester 2026.

Das Projekt untersucht, inwieweit die Ausgaben von Large Language Models in der explorativen
Datenanalyse mit dem tatsächlich bereitgestellten Datensatz übereinstimmen. Dazu werden die
Antworten zweier Modelle mit Referenzwerten verglichen, die auf denselben Eingabedaten mit
etablierten statistischen Verfahren berechnet wurden. Die Modelle erhalten den Datensatz als
Text im Kontext und verfügen über kein externes Rechenwerkzeug.

## Untersuchungsaufbau

| Experiment | Datengrundlage       | Fragen                                                           | Wiederholungen |
| ---------- | -------------------- | ---------------------------------------------------------------- | -------------- |
| E0         | ohne Datensatz       | 15 konzeptionelle Fragen zum Vorgehen der EDA                    | 3              |
| E1         | Originaldatensatz    | 20 Fragen (10 faktisch, 5 interpretativ, 5 Halluzinationsfallen) | 5              |
| E2         | manipulierte Fassung | derselbe Katalog wie E1                                          | 5              |

Ergänzend prüft eine Zusatzabfrage (`E2_probe`) gezielt die Kündigungsquote nach `OverTime`
auf der manipulierten Fassung. Sie wurde ausschließlich für OpenAI durchgeführt.

Untersuchte Modelle: `gpt-5.6-luna` (OpenAI) und `gemini-3.6-flash` (Google).
Einheitliche Parameter: `temperature = 1`, `max_tokens = 8000`.
Der Datensatz wird bei OpenAI jeder Anfrage vorangestellt und bei Google über einen
expliziten Kontext-Cache bereitgestellt (`cache_ttl = 7200`).

## Projektstruktur

```
code/
├── Bewertung/
│   ├── Bewertungsrubrik.md          Bewertungskriterien je Fragekategorie
│   ├── E0_Kodierung.xlsx            Kodierung und Punktwerte Experiment 0
│   └── E1+E2_Kodierung.xlsx         Kodierung und Punktwerte Experiment 1 und 2
├── data/
│   ├── archiv/                      frühere Datenstände aus einzelnen Referenzwerten
│   ├── datensatz_meta.json          Metadaten und SHA-256-Prüfwerte der Datenfassungen
│   ├── ibm_original.csv             unveränderter Datensatz, 1470 Zeilen, 35 Spalten
│   ├── ibm_manipuliert.csv          manipulierte Fassung, OverTime permutiert
│   ├── referenzwerte.json           Referenzwerte zum Originaldatensatz
│   └── referenzwerte_manipuliert.json   Referenzwerte zur manipulierten Fassung
├── fragenkataloge/
│   ├── experiment0.json             Fragenkatalog E0, maschinenlesbar
│   ├── experiment1.json             Fragenkatalog E1 und E2, maschinenlesbar
│   ├── Fragen Ex0.md                Fragenkatalog E0, lesbare Fassung
│   └── Fragen Ex1.md                Fragenkatalog E1 und E2, lesbare Fassung
├── results/
│   ├── E0_answers.jsonl             Antworten Experiment 0
│   ├── E1_answers.jsonl             Antworten Experiment 1
│   ├── E2_answers.jsonl             Antworten Experiment 2
│   ├── E2_probe_answers.jsonl       Antworten der Zusatzabfrage zu E2
│   └── (Testläufe und verworfene Stände, siehe unten)
├── datensatz_exploration.ipynb      Aufbereitung und Berechnung der Referenzwerte
├── E2_manipulation.ipynb            Erzeugung der manipulierten Datenfassung
├── experiments.ipynb                Durchführung der Experimente (Runner)
├── llm_client.py                    einheitlicher Zugriff auf beide Anbieter
├── config.py                        Modellnamen und Laufzeitparameter
├── notizen_datensatz.md             Notizen zur Datengrundlage
├── referenzwerte.csv                Referenzwerte als flache Tabelle
├── requirements.txt                 Python-Abhängigkeiten
└── .env                             API-Schlüssel, nicht versioniert
```

## Einrichtung

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Die Datei `.env.example` nach `.env` kopieren und die eigenen Zugangsdaten
eintragen. Benötigt werden `OPENAI_API_KEY` und `GOOGLE_API_KEY`. Die `.env`
enthält Geheimnisse und gehört nicht in die Versionsverwaltung.

## Ablauf einer vollständigen Reproduktion

1. **Referenzwerte berechnen.** `datensatz_exploration.ipynb` vollständig ausführen. Das
   Notebook entfernt die drei Spalten ohne Varianz (`EmployeeCount`, `StandardHours`,
   `Over18`), ergänzt die numerischen Hilfsvariablen `Attrition_num` und `OverTime_num` und
   schreibt `referenzwerte.json`.

2. **Manipulierte Fassung erzeugen.** `E2_manipulation.ipynb` ausführen. Es permutiert die
   Spalte `OverTime` unter Erhalt beider Randverteilungen und schreibt
   `ibm_manipuliert.csv`.

3. **Referenzwerte der manipulierten Fassung berechnen.** `datensatz_exploration.ipynb`
   erneut ausführen, mit `ibm_manipuliert.csv` als Eingabe und
   `referenzwerte_manipuliert.json` als Ausgabe. Der Kernel muss dafür neu gestartet und das
   Notebook von oben durchlaufen werden.

4. **Experimente durchführen.** `experiments.ipynb` ausführen. Der Runner schreibt jede
   Antwort einzeln nach `results/`. Bereits vorhandene Kombinationen aus Experiment, Frage,
   Modell und Iteration werden übersprungen, sodass ein unterbrochener Lauf fortgesetzt
   werden kann, ohne bestehende Antworten erneut anzufragen.

5. **Bewerten.** Die Antworten werden manuell in den Excel-Dateien unter `Bewertung/`
   kodiert, nach den Kriterien in `Bewertungsrubrik.md`.

## Die Manipulation

Verändert wird ausschließlich die Beziehung zwischen `OverTime` und `Attrition`. Die Spalte
`OverTime` wird mit festem Zufalls-Seed neu zugeordnet, wobei die Zahl der Beschäftigten mit
und ohne Überstunden unverändert bleibt (416 und 1054) und die Spalte `Attrition` überhaupt
nicht angefasst wird. Dadurch bleiben beide Randverteilungen und die Gesamtkündigungsquote
identisch, während sich die Richtung des Zusammenhangs umkehrt.

| Datenfassung | Kündigungsquote bei `OverTime = Yes` | bei `OverTime = No` |
| ------------ | ------------------------------------ | ------------------- |
| Original     | 30,5 %                               | 10,4 %              |
| Manipuliert  | 7,9 %                                | 19,4 %              |

Von 54 berechneten Referenzwerten ändern sich dadurch genau drei: die Kündigungsquote nach
`OverTime`, die Korrelation von `OverTime_num` mit `Attrition_num` (von +0,2461 auf −0,1399,
womit die Variable aus den fünf stärksten Korrelationen ausscheidet) und die Assoziationsregel
zu `OverTime`.

Alle übrigen Kennzahlen bleiben unverändert. Das ist beabsichtigt und ermöglicht es, eine
beobachtete Abweichung eindeutig der Manipulation zuzuordnen.

## Aufbau der Ergebnisdateien

Die Dateien unter `results/` liegen im JSON-Lines-Format vor, eine Antwort je Zeile:

```json
{
  "experiment": "E1",
  "question_id": "E1_A01",
  "category": "A",
  "iteration": 1,
  "provider": "openai",
  "model": "gpt-5.6-luna",
  "model_version": "gpt-5.6-luna",
  "prompt": "[dataset + question]",
  "answer": "...",
  "input_tokens": 115665,
  "cached_tokens": 0,
  "output_tokens": 62,
  "temperature": 1.0,
  "finish_reason": "stop",
  "timestamp": "2026-08-20 11:04:50"
}
```

Das Feld `prompt` enthält einen Platzhalter statt des vollständigen Prompts, da der Datensatz
jeder Anfrage vorangestellt wird und die Dateien sonst unhandlich groß würden. Der tatsächlich
gesendete Inhalt ergibt sich aus dem Fragenkatalog und der jeweiligen Datenfassung.

Das Feld `finish_reason` ist für die Auswertung wesentlich. Der Wert `MAX_TOKENS` kennzeichnet
eine am Ausgabelimit abgeschnittene Antwort. In Experiment 1 betrifft das elf Antworten,
sämtlich bei Gemini.

## Nicht verwendete Dateien in `results/`

Diese Dateien stammen aus Vorläufen und gehen nicht in die Auswertung ein:

- `deprecated_E1_answers.jsonl` – verworfener Stand von Experiment 1
- `E0_answers_cappedRateLimit.jsonl` – durch Ratenbegrenzung unvollständiger Lauf
- `E0_TEST.jsonl` und `E1_MINI_answers.jsonl` – Testläufe mit verkürztem Fragenkatalog

## Datengrundlage

IBM HR Analytics Employee Attrition and Performance, ein öffentlich verfügbarer, synthetisch
erzeugter Datensatz mit 1470 Beobachtungen und 35 Variablen. Die Kündigungsquote liegt bei
etwa 16 Prozent.

## Zentrale Parameter

Sämtliche Festlegungen der Untersuchung stehen als benannte Konstanten in `config.py` und werden von den Notebooks importiert. Die Notebooks setzen keine eigenen Werte. Wer einen Parameter verändern möchte, ändert ihn dort und nur dort.

| Konstante            | Wert | Bedeutung                                                              |
| -------------------- | ---- | ---------------------------------------------------------------------- |
| `SEED`               | 42   | Zufalls-Seed der Permutation in Experiment 2                           |
| `TARGET_YES_LEAVERS` | 33   | Zahl der Gekündigten, die der Gruppe mit Überstunden zugeordnet werden |
| `TEMPERATURE`        | 1    | bei GPT vorgegeben, bei Gemini entsprechend gesetzt                    |
| `MAX_OUTPUT_TOKENS`  | 8000 | maximale Antwortlänge                                                  |
| `CACHE_TTL_SECONDS`  | 7200 | Lebensdauer des expliziten Kontext-Caches bei Google                   |
| `ITERATIONS_EXP0`    | 3    | Wiederholungen in Experiment 0                                         |
| `ITERATIONS_DATA`    | 5    | Wiederholungen in Experiment 1 und 2                                   |
| `IQR_FACTOR`         | 1,5  | Schwellenwert der Ausreißerbestimmung                                  |
| `N_BINS`             | 3    | quantilsbasierte Einteilung in niedrig, mittel, hoch                   |
| `MIN_SUPPORT`        | 0,05 | Mindestsupport der Regelgenerierung                                    |
| `MIN_IMPROVEMENT`    | 0,05 | Minimal Improvement nach Hammesfahr und Spott (2021)                   |
| `TOLERANCE_FULL`     | 0,02 | relative Abweichung bis 2 %, volle Punktzahl                           |
| `TOLERANCE_PARTIAL`  | 0,05 | relative Abweichung bis 5 %, ein Punkt                                 |

Die Mindestkonfidenz der Regelgenerierung ist kein fester Wert, sondern wird
als Median der Konfidenzen der Ausgangsregelmenge bestimmt.

### Seed und Reproduzierbarkeit

Die Manipulation in Experiment 2 ist der einzige Schritt mit einer
Zufallskomponente. Sie ordnet die Spalte `OverTime` neu zu und lässt dabei
beide Randverteilungen unverändert. Mit `SEED = 42` und
`TARGET_YES_LEAVERS = 33` entsteht dieselbe Zuordnung bei jedem Lauf; die
Kreuztabelle von `OverTime` und `Attrition` lässt sich als Kontrolle
heranziehen und muss 850, 204, 383 und 33 ergeben.

Die Anfragen an die Modelle sind demgegenüber nicht reproduzierbar, da beide
mit einer Temperatur von 1 angefragt werden. Ein erneuter Lauf erzeugt andere
Antworten und damit andere Punktwerte. Die in der Arbeit berichteten Ergebnisse
beruhen auf den gespeicherten Antworten unter `results/`.

### Bewertungsparameter

`TOLERANCE_FULL` und `TOLERANCE_PARTIAL` dokumentieren die in der Arbeit
festgelegten Toleranzbänder für die faktischen Fragen. Die Bewertung selbst
erfolgt manuell in den Excel-Dateien unter `Bewertung/`; die Konstanten werden
im Code nicht ausgewertet und stehen dort ausschließlich zur Dokumentation.
