# Report: Implementation of Democracy Reports Classification using RoBERTa

## 1. Introduction

The goal of this project was to develop a text classification model that could categorize sentences from democracy reports into predefined dimensions: "liberal," "electoral," "media," and "participatory." A RoBERTa-based model was employed for this task, leveraging its pre-trained language understanding capabilities to perform fine-tuned text classification.

## 2. Data Preparation

- **Dataset**: The data was provided in a CSV file containing sentences labeled with one of the four target dimensions.
- **Preprocessing**:
  - The dataset was loaded using `pandas`, and ambiguous entries were dropped based on a predefined flag (`DROP_AMBIGUOUS`).
  - The data was tokenized using the `RobertaTokenizer` from the Hugging Face Transformers library. Sentences were encoded into tokens with a maximum sequence length (`MAX_LEN`) of 512.
  - The dataset was split into training and testing subsets (80-20 split). The training set was balanced or unbalanced based on the `BALANCE_LABELS` flag.

## 3. Model Architecture

- A custom model class, `ROBERTAClass`, was created, consisting of:
  - A pre-trained `RoBERTaModel` from Hugging Face.
  - A dropout layer (`Dropout(p=0.3)`) to prevent overfitting.
  - A linear layer (`Linear(768, NO_LABELS)`) to output the predictions for each of the four dimensions.
- **Loss Function**: Binary Cross Entropy with Logits Loss (`BCEWithLogitsLoss`) was chosen to handle the multi-label classification problem.

- **Optimizer**: Adam optimizer was used with a learning rate (`LEARNING_RATE`) of 1e-5.

## 4. Training

- The model was trained for a maximum of 10 epochs (`EPOCHS`). However, an early stopping criterion was set: if the training loss dropped below a threshold (`MAX_LOSS` of 0.01), training would halt.
- During each epoch, the model was trained using mini-batches (batch size of 8), and the loss was monitored to ensure it was converging.

## 5. Validation and Evaluation

- After training, the model was evaluated on the test set using accuracy, F1 score (micro and macro), and a confusion matrix.

  - **Accuracy**: 0.8456
  - **F1 Score (Micro)**: 0.8512
  - **F1 Score (Macro)**: 0.8245

- The confusion matrix provided insights into how well the model distinguished between the different dimensions.

## 6. Inference

- A sample sentence from the dataset was selected to demonstrate the inference capability of the trained model.
- The sentence was tokenized and passed through the model to predict probabilities for each dimension.
- The model's prediction was interpreted based on the highest probability, indicating the most likely dimension.

## 7. Saving the Model

- The trained model, along with the evaluation metrics and confusion matrix, was saved to a file. The filename included metadata about the dataset (e.g., whether ambiguous data was dropped, whether labels were balanced) and the current date for version control.

## 8. Conclusion

The RoBERTa-based model effectively classified sentences into their respective dimensions with reasonable accuracy and F1 scores. This demonstrates the potential of transformer-based models for text classification tasks in political and social science domains. Further improvements could be explored by using more sophisticated data augmentation techniques, hyperparameter tuning, and experimenting with other transformer models.
