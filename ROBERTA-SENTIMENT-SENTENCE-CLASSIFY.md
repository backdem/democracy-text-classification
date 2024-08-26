## Implementation of Sentiment Analysis using ROBERTA Model

### Introduction
To classify sentences in the corpus regarding their sentiment towards democracy backsliding, a fine-tuned ROBERTA model was implemented. The objective was to determine the sentiment expressed in each sentence—whether it is positive, negative, neutral, or ambivalent about democracy.

### Data Preparation
The initial step involved preparing the dataset for training. The corpus consisted of sentences labeled for sentiment regarding democracy backsliding:

- The labels were:
  - 1 = Positive
  - 2 = Negative
  - 3 = Neutral
  - 4 = Ambivalent (both positive and negative statements in one sentence)
  - 0 = Ambiguous (unclear relation to democracy)
- Labels 4.0 and 0 were excluded from the dataset to focus on clearer sentiment categories.
- The cleaned dataset was vectorized using a custom function `get_vectorized_labelled_data`, which generated vector representations for the sentences.

### Model Architecture
A custom model was built on top of the pre-trained `roberta-base` model from Hugging Face’s Transformers library:

- **ROBERTA Model Layer**: The core component is the `RobertaModel` which generates contextualized word embeddings for the input text.
- **Dropout Layer**: A dropout layer with a probability of 0.3 was added to prevent overfitting during training.
- **Linear Output Layer**: A fully connected layer maps the output to the number of sentiment labels.

### Training the Model
The training process was configured with the following parameters:

- **Batch Size**: Training batch size of 8 and validation batch size of 4.
- **Epochs**: The model was trained for up to 10 epochs, with early stopping if the loss fell below a threshold of 0.01.
- **Learning Rate**: A learning rate of \(1 \times 10^{-5}\) was used.

Training involved:

- **Loss Function**: Binary Cross-Entropy Loss with Logits was used to handle the multi-label classification problem.
- **Optimization**: The Adam optimizer was employed to adjust the model weights.
- **Device Utilization**: Training was performed on a GPU (if available) to accelerate the computation.

### Model Evaluation
The model was evaluated using a separate test set:

- **Performance Metrics**:
  - Accuracy: The proportion of correctly predicted labels.
  - F1 Score (Micro and Macro): The harmonic mean of precision and recall, measured both globally (micro) and per-class (macro).
- **Confusion Matrix**: A confusion matrix was generated to visualize the performance across different sentiment categories.

Validation results showed the model's capability to accurately classify sentences according to the sentiment expressed towards democracy.

### Inference and Prediction
The trained model was tested with sample sentences to predict their sentiment:

- Sentences were tokenized and encoded using the `RobertaTokenizer`.
- The model output probabilities for each sentiment class, which were interpreted using a threshold of 0.5.

### Saving the Model
The final trained model, along with the evaluation metrics and confusion matrix, was saved for future use:

- The model was saved using PyTorch’s `torch.save` functionality, preserving the entire model architecture and weights.
- Evaluation results were stored in a text file to document model performance.
