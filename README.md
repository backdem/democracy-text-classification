# democracy-text-classification

Fine tune LLM for text classifcation on democracy labels. The [/notebooks](./notebooks/) you will find a collection o f notebooks used to fine-tune a classifier
for sentence classification. The models tried where BERT, legal-BERT, DeBERTa and RoBERTa. After initial accuracy from all models, RoBERTa performed the best
and we focused solely on RoBERTa. We implemented 2 classifiers one for classifying demcoracy dimensions and another for classifying democracy sentiment.

More details about the implementation approaches of these classifiers are found here:

- Classify demcoracy dimensions [ROBERTA-DIMENSION-SENTENCE-CLASSIFY.md](./ROBERTA-DIMENSION-SENTENCE-CLASSIFY.md)
- Classify democracy sentiment [ROBERTA-SENTIMENT-SENTENCE-CLASSIFY.md](./ROBERTA-SENTIMENT-SENTENCE-CLASSIFY.md)
