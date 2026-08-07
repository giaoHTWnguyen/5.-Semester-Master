# Bewertungsrubrik – Experiment 0 (EDA-Konzeptwissen)

Skala je Frage: **0–3 Punkte**

| Punkte | Bedeutung                                                                                    |
| :----: | -------------------------------------------------------------------------------------------- |
| **3**  | vollständig korrekt: alle Kernpunkte genannt, fachlich fehlerfrei                            |
| **2**  | weitgehend korrekt: Kernpunkte im Wesentlichen erfasst, kleinere Lücken oder Ungenauigkeiten |
| **1**  | teilweise korrekt: nur einzelne Kernpunkte, deutliche Lücke oder ein fachlicher Fehler       |
| **0**  | falsch oder ohne substanziellen Inhalt                                                       |

## Erwartete Kernpunkte je Frage

| ID    | Thema                                             | Erwarteter Kernpunkt                                                                                                                                                                                                                                 |
| ----- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E0_01 | Schritte der EDA                                  | Formale Erfassung/Variablentypen, univariate Analyse (Lage, Streuung), bi-/multivariate Zusammenhänge, Prüfung fehlender/inkonsistenter Werte, Ausreißererkennung, Feature Engineering, iterativer Charakter (Deckung mit Rahmany)                   |
| E0_02 | IQR-Methode                                       | IQR = Q3 − Q1; Ausreißergrenzen bei Q1 − 1,5·IQR und Q3 + 1,5·IQR; robust gegenüber Extremwerten, da auf Quartilen basierend                                                                                                                         |
| E0_03 | Mittelwert, Median, Modus                         | Mittelwert = arithmetisches Mittel (empfindlich für Ausreißer); Median = mittlerer Wert (robust); Modus = häufigster Wert (auch kategorial); Bezug zu Skalenniveaus                                                                                  |
| E0_04 | Uni-, bi-, multivariat                            | Univariat = eine Variable (Verteilung/Lage/Streuung); bivariat = Zusammenhang zweier Variablen; multivariat = mehrere Variablen gleichzeitig                                                                                                         |
| E0_05 | Median statt Mittelwert                           | Bei schiefen Verteilungen, bei Ausreißern, bei ordinalen Daten; zentrales Argument ist die Robustheit des Medians                                                                                                                                    |
| E0_06 | Boxplot vs. Histogramm                            | Boxplot für Lage, Streuung, Ausreißer und kompakten Gruppenvergleich; Histogramm für die Form der Verteilung (Modalität, Schiefe, Lücken), die der Boxplot verbirgt                                                                                  |
| E0_07 | Kennzahlen kategorial vs. metrisch                | Kategorial = Häufigkeiten, Modus, Balkendiagramm, Kontingenztabelle; metrisch = Mittelwert/Median, Streuungsmaße, Histogramm/Boxplot                                                                                                                 |
| E0_08 | Transformation erkennen                           | Bei starker Schiefe oder wachsender Streuung um die Gerade (Heteroskedastizität); Ziel ist Annäherung an Symmetrie/Normalverteilung; Log-Transformation für rechtsschiefe oder multiplikative Daten                                                  |
| E0_09 | Was Korrelation nicht aussagt                     | Keine Kausalität; Pearson erfasst nur lineare Zusammenhänge; anfällig für Ausreißer; Scheinkorrelation/Störfaktor möglich. Kernfehler: Gleichsetzung von Korrelation und Kausalität                                                                  |
| E0_10 | Ausreißer entfernen problematisch                 | Ausreißer können echte, informative Fälle sein; Entfernen verzerrt Ergebnisse; Entscheidung sollte von Ursache (Messfehler vs. echter Extremfall), Domänenwissen und Analyseziel abhängen                                                            |
| E0_11 | Korrelation nahe null                             | Pearson misst nur lineare Zusammenhänge; ein nichtlinearer Zusammenhang kann trotz Koeffizient nahe null bestehen; Streudiagramm zur Prüfung nötig                                                                                                   |
| E0_12 | Zu viele Hypothesen an denselben Daten            | Problem des multiplen Testens (p-Hacking); steigende Rate falsch positiver Befunde; explorative Ergebnisse sind hypothesengenerierend, nicht bestätigend; unabhängige Validierung nötig                                                              |
| E0_13 | EDA nicht rein automatisierbar                    | Erfordert geeignete Fragen, Domänen- und Kontextwissen, interpretatives Urteil; iterativer Charakter; Rolle der analysierenden Person (Deckung mit Langer)                                                                                           |
| E0_14 | Visualisierungsauswahl beeinflusst Interpretation | Achsenskalierung (linear vs. logarithmisch, abgeschnittene Achsen) und Bin-Breite verändern die wahrgenommene Verteilung/Modalität; Bewusstsein für irreführende Darstellungen                                                                       |
| E0_15 | Schiefe (Skewness)                                | Bei Schiefe fallen Mittelwert, Median und Modus auseinander; der Mittelwert wird durch den Ausläufer verzerrt, daher ist bei starker Schiefe der Median robuster; rechtsschiefe Daten können durch Wurzel- oder Log-Transformation angenähert werden |

## Hinweise zur Anwendung

- Die Kernpunkte sind der Bewertungsmaßstab und werden dem Modell **nicht** vorgelegt.
- Bei Doppelfragen (z. B. E0_06 „wann umgekehrt") müssen für die volle Punktzahl **beide** Seiten erfasst sein.
- Über die drei Wiederholungen je Frage wird zusätzlich die Konsistenz betrachtet (Streuung der Punktzahlen).
