# Survey of Hallucination in Natural Language Generation

## Was ist die Hauptaussage?

Die Hauptaussage ist die Bereitstellung eines ersten Umfassenden Überblicks über das Problem der Halluzinationen in der computergestützten Generierung natürlicher Sprache. Der Text verdeutlicht, dass moderne Deep-Learning-Modelle zwar flüssige Texte produzieren, aber oft Inhalte generieren, die nicht mit der Eingabequelle übereinstimmen oder faktisch falsch sind, Was die Leistung und Sicherheit dieser Systeme beeinträchtigt.

## Was ist relevant für MEINE Arbeit?

- Definition und Kategorisierung: Halluzinationen werden als Texte definiert, die ungetreu (unfaithful) oder unsinning in Bezug auf die bereitgestellte Quelle sind. Es wird zwischen intrinsischen Halluzinationen (Widerspruch zur Quelle) und extrinsischen Halluzinationen (Informationen, die weder durch die Quelle belegt noch direkt widerlegt werden können) unterschieden.
- Ursachenforschung: Der Text identifiziert verschiedene Fehlerquellen, die zu Halluzinationen führen, darunter Probleme in den Datensätzen (wie Abweichungen zwischen Quelle und Referenztext) sowie Schwachstellen im Training und bei den Inferenzmethoden der Modelle
- Analyse von Messgrößen und Gegenmaßnahmen: Die Autoren geben eine Übersicht über statistische und modellbasierte Metriken zur Messung von Halluzinationen sowie über Methoden zu deren Verringerung, etwa durch die Bereinigung der Trainingsdaten oder Anpassung an der Modellarchitektur
- Fokus auf große Sprachmodelle (LLMS): ein wesentlicher Teil befasst sich mit den spezifischen Herausforderungen von LLMs, bei denen Halluzinationen aufgrund ihres enormen Wissens und ihrer Überzeugungskraft besonders schwer zu identifizieren sind

## Konkrete Stelle / Zitat (mit Seitenzahl!)

S. 5: "..." → relevant weil...

S. 4: "Hallucinated Text gives the impression of being fluent and natural despite being unfaithful and nonsensical. It appears to be grounded in the real context provided, although it is actually hard to specify or verify the other "real" preceptions, hallucinated text is also hard to capture at first glance. Withhin the context of NLP, the above definition of hallucination, the generated content that is nonsensical or unfaithful to the provided source content, is the most inclusive and standard." -> Definition Halluzination

s.4: "(1) Intrinsic Halllucinations: The generated output that contradicts the source content. For instance, in the abstractive summarization task from Table 1, the generated summary "The first Evola vaccine was approved in 2021" contradicts the source content "The first vaccine for Ebola was approved by the FDA in 2019."
(2) Extrinsic Hallucination: The generated output cannot be verified from the source content (i.e., output that can neither be supported nor contradicted by the source). For example, in the abstractive summarization task from Table 1, the information “China has already started clinical trials of the COVID-19 vaccine.” is not mentioned in source. We can neither find evidence for the generated output from the source nor assert that it is wrong. Notably, the extrinsic hallucination is not always erroneous because it could be from factually correct external information [177, 247]. Such factual hallucination can be helpful because it recalls additional background knowledge to improve the informativeness of the generated
text. However, in most of the literature, extrinsic hallucination is still treated with caution because its unverifiable aspect of this additional information increases the risk from a factual safety perspective. " -> Beispiel Kategorisierung von Halluzination

S.5: "When collecting large-scale datasets, some works heuristically select
and pair real sentences or tables as the source and target [132, 283]. As a result, the target reference
may contain information that cannot be supported by the source [198, 268]. For instance, when constructing WIKIBIO [132], a dataset for generating biographical notes based on the infoboxes
of Wikipedia, the authors took the Wikipedia infobox as the source and the first sentence of the
Wikipedia page as the target ground-truth reference. However, the first sentence of the Wikipedia
article is not necessarily equivalent to the infobox in terms of the information they contain. Indeed,
Dhingra et [45] points out that 62% of the first sentences in WIKIBIO have additional information
not stated in the corresponding infobox. Such mismatch between source and target in datasets can
lead to hallucination." --> Beispiel Problem mit der Arbeit von Large-Scale Datasets

S.8 Ursachenforschung: "The encoder has the role of comprehending and encoding input text into meaningful representations. An encoder wit ha defective comprehension ability could influence the degree of hallucination [198]. When encoders learn wrong correlations between different parts of the training data, it could result in erroneous generation that diverges from the input"

S. 8 Ursachenforschung Erreoneous decoding: "We conjecture that deliberately added "randomness" by sampling from the top-k samples instead of choosing the post probable token increase the unexpected nature of the generation, leading to a higher chance of containing hallucinated content.""

s.8 Ursachenforschung Exposure Bias: "... it is common practice to train the decoder with ... MLE taining where the decoder is encouraged to predict the next token conditioned on the ground-truth prefix sequences. However, during the inference generation, the model generates the next token conditioned on the historical sequences previously generated by itself."

s.8/9 Parametric knowledge bias: "Pre-training of models on a large corpus is known to result in the model memorizing knowledge in its parameters. .... it helps prove the performance of downstream tasks but also serves as another contributor to hallucinatory generation. Large pre-trained models ... are powerful in providing generalizability and coverage but Longpre et al. have discovered that such models prioritize parametric knowledge over the provided input"

S.9 what does recent research works show?: "works highlight a discrepancy between surface realization and inherent knowledge of the model in NLG tasks. Models can realize they are generating something hallucinated in some way"

S.10 Metrics Measuring Hallucination but for quality of writing

"Area Under the ROC Curve, F1-score"

S.36

"...hallucination takes on a broader definition than before because of the vastness of training data, the breadth of knowledge base, and multitasking capability. ... Consequently, hallucination in LLMs not only signifies deviations from the source input but also extends to deviations from training data, marking it more oriented towards the Extrinsic type"

## Offene Fragen die das Paper aufwirft

- Gilt das auch speziell für Datenanalyse-Kontexte?
- Haben neuere Modelle (GPT-4, Claude) das verbessert?
- Können Modelle nachvollziehen oder reflektieren, dass sie in der EDA halluzinieren?
- Welche Parameter sind besonders stark, damit ein Model dieses parametric Wissen über dem provided input prioritisiert?
