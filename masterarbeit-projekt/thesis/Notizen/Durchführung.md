## Referenzanalyse Wirtschaftsinformatik

1. Der Datensatz ist nicht definiert
   Du musst konkret sagen: welcher Datensatz, warum genau dieser, wie wird er manipuliert. Das ist das Herzstück deiner Methodik.

## Experimente durchführen

FF1 + FF2 → Experiment 1: Referenzanalyse
FF1 → Experiment 2: Original vs. manipulierter Datensatz  
FF3 → Experiment 3: Einmalige vs. iterative Interaktion
FF4 → Experiment 0: Wissenstest (vor den anderen)

3. Das Evaluationsframework ist noch zu unscharf
   "±5%" ist ein Anfang, aber du brauchst ein Scoring. Zum Beispiel:
   Faktische Korrektheit:
   2 Punkte = korrekt (innerhalb ±5%)
   1 Punkt = teilweise korrekt (±5–20%)
   0 Punkte = falsch (>±20% oder komplett erfunden)

4. FF4 "Wie viel Wissen haben LLMs über EDA?" hat kein Experiment
   Das ist eigentlich ein separater Test bevor du anfängst: Du fragst das LLM gezielt nach EDA-Konzepten ohne Daten zu geben und bewertest die Antworten.

## Durchführung einer klassischen Explorativen Datenanalyse

inhaltliche Phasen

- Prüfung fehlender Werte, inkonsistente Schreibweisen und ungeeignete Datentypen

- erste deskriptiven Statistiken (Mittelwerte, Mediane, Standardabweichungen)

Referenzanalyse

- manuelle Analyse des Datensatzes
- Bewertung der EDA
