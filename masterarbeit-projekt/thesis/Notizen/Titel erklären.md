# Titel der Arbeit erklären

**„Untersuchung von LLMs auf Datenkonsistenz und Zuverlässigkeit in der explorativen Datenanalyse“**

## Datenkonsistenz

### Was meine ich damit?

Mit **Datenkonsistenz** ist in meiner Arbeit vor allem die Übereinstimmung zwischen der **konkret bereitgestellten Datengrundlage** und den daraus vom LLM abgeleiteten Aussagen gemeint.

Es geht also nicht primär um Datenkonsistenz im klassischen Datenbank-Sinn, sondern um die Frage:

> **Passt die Antwort des Modells zu den Daten, die ich ihm tatsächlich gegeben habe?**

Dazu gehören beispielsweise:

- genannte Kennzahlen,
- identifizierte Zusammenhänge,
- Aussagen über Gruppen,
- Interpretationen der Ergebnisse.

### Beispiel aus meiner Arbeit

Besonders deutlich wird dies in Experiment 2.

Im ursprünglichen Datensatz gilt:

- `OverTime = Yes`: ca. 30,5 % Attrition
- `OverTime = No`: ca. 10,4 % Attrition

Im manipulierten Datensatz wurde dieser Zusammenhang gezielt umgekehrt:

- `OverTime = Yes`: ca. 7,9 % Attrition
- `OverTime = No`: ca. 19,4 % Attrition

Wenn ein Modell trotz des manipulierten Datensatzes behauptet, dass Beschäftigte mit `OverTime = Yes` häufiger kündigen, stimmt die Aussage **nicht mit der konkret bereitgestellten Datengrundlage überein**.

**Merksatz:**

> **Datenkonsistenz = Passt die Modellaussage zu den tatsächlich bereitgestellten Daten?**

---

## Zuverlässigkeit

### Was meine ich damit?

**Zuverlässigkeit** ist in meiner Arbeit breiter als die reine Korrektheit einer einzelnen Antwort.

Es geht darum, ob ein LLM unter den untersuchten Bedingungen **verlässliche Analyseergebnisse** liefert.

Dazu gehören insbesondere:

- inhaltliche Korrektheit,
- Übereinstimmung mit der Datengrundlage,
- Reproduzierbarkeit über wiederholte Anfragen,
- keine nicht durch die Daten gedeckten Behauptungen.

**Merksatz:**

> **Zuverlässigkeit = Kann ich mich unter den untersuchten Bedingungen auf die Analyse des Modells verlassen?**

---

## Reproduzierbarkeit ist nicht dasselbe wie Zuverlässigkeit

Ein Modell kann sehr **reproduzierbar** sein und trotzdem falsch liegen.

### Beispiel A06

Bei Gemini ergibt sich bei der Ausreißerfrage:

- mittlerer Punktwert: 0
- Standardabweichung: 0

Das bedeutet:

Das Modell erzielt über die Wiederholungen hinweg stabil dieselbe Bewertung, liegt aber trotzdem falsch.

**Merksatz:**

> **Konsistenz bzw. Reproduzierbarkeit bedeutet Stabilität, nicht automatisch Korrektheit.**

---

## Verhältnis von Datenkonsistenz und Zuverlässigkeit

Ich würde mir den Unterschied so merken:

> **Datenkonsistenz fragt: Passt die Antwort zu meinen Daten?**

> **Zuverlässigkeit fragt: Kann ich mich insgesamt auf die Analyse verlassen?**

Datenkonsistenz ist damit eine zentrale Voraussetzung für eine zuverlässige LLM-gestützte EDA.

Eine Antwort kann beispielsweise:

- **plausibel, aber nicht datentreu** sein,
- **reproduzierbar, aber falsch** sein,
- **methodisch überzeugend, aber auf die konkreten Daten falsch angewendet** sein.

Genau deshalb reicht es nicht aus, nur zu untersuchen, ob eine Antwort plausibel klingt.

---

# Zusammenhang mit den drei Experimenten

## Experiment 0 – Methodisches Vorwissen

Frage:

> **Weiß das Modell grundsätzlich, wie EDA funktioniert?**

Ergebnis:

Beide Modelle zeigen ein sehr hohes methodisches Vorwissen.

Bedeutung:

> **Methode kennen bedeutet nicht automatisch, sie auf einen konkreten Datensatz korrekt anzuwenden.**

---

## Experiment 1 – Analyse des Originaldatensatzes

Frage:

> **Wie korrekt und datengestützt analysieren die Modelle den konkret bereitgestellten Datensatz?**

Hier werden unter anderem betrachtet:

- faktische Kennzahlen,
- Interpretationen,
- Reproduzierbarkeit,
- Halluzinationsfallen,
- durch die Daten gedeckte bzw. nicht gedeckte Aussagen.

---

## Experiment 2 – Manipulierter Datensatz

Frage:

> **Bleiben die Modelle der konkret bereitgestellten Datengrundlage treu, wenn diese vom ursprünglichen bzw. erwartbaren Zusammenhang abweicht?**

Der OverTime–Attrition-Zusammenhang wird gezielt umgekehrt.

Trotzdem geben die Modelle überwiegend bzw. vollständig den ursprünglichen Zusammenhang wieder.

Damit ist Experiment 2 ein besonders deutliches Beispiel für fehlende Datentreue.

---

# Wenn der Prüfer sagt: „Erklären Sie Ihren Titel.“

## Mögliche Antwort

> Im Kern untersuche ich, ob LLMs bei einer explorativen Datenanalyse tatsächlich Aussagen treffen, die mit der konkret bereitgestellten Datengrundlage übereinstimmen, und wie zuverlässig dieses Verhalten ist.
>
> Unter Datenkonsistenz verstehe ich dabei vor allem die Übereinstimmung zwischen den bereitgestellten Daten und den daraus abgeleiteten Kennzahlen, Zusammenhängen und Interpretationen.
>
> Zuverlässigkeit ist etwas breiter. Es geht nicht nur darum, ob eine einzelne Antwort korrekt ist, sondern auch darum, ob das Antwortverhalten über Wiederholungen stabil und durch die Daten gedeckt bleibt.
>
> Meine Ergebnisse zeigen, warum diese Unterscheidung wichtig ist: Ein Modell kann beispielsweise sehr reproduzierbar antworten und trotzdem reproduzierbar falsch liegen.

---

# Wenn anschließend gefragt wird: „Haben Sie ein Beispiel?“

> Ja. Besonders deutlich wird das in Experiment 2. Dort habe ich den Zusammenhang zwischen `OverTime` und `Attrition` gezielt umgekehrt. Im manipulierten Datensatz haben Beschäftigte mit `OverTime = Yes` eine niedrigere Kündigungsquote. Trotzdem geben die Modelle überwiegend beziehungsweise vollständig den ursprünglichen Zusammenhang wieder.
>
> Das Antwortverhalten kann also sehr konsistent sein, stimmt aber nicht mit der tatsächlich bereitgestellten Datengrundlage überein.

---

# Ultra-Kurzfassung

**Datenkonsistenz:**

> Passt die Antwort zu den konkret bereitgestellten Daten?

**Zuverlässigkeit:**

> Kann ich mich unter den untersuchten Bedingungen auf die Analyse verlassen?

**Wichtigster Unterschied:**

> Ein Ergebnis kann reproduzierbar sein und trotzdem falsch oder nicht datentreu sein.

**Bestes Beispiel:**

> Experiment 2: Daten wurden gezielt verändert, die Modelle geben trotzdem den ursprünglichen Zusammenhang wieder.
