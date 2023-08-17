# import transformers
#
#
# def sentiment_analysis(text):
#     """Performs sentiment analysis on a piece of text using DistilBERT."""
#
#     # Load the DistilBERT model and tokenizer.
#     model = transformers.DistilBertModel.from_pretrained("distilbert-base-uncased", return_dict=False)
#     tokenizer = transformers.DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
#
#     # Encode the text using the tokenizer.
#     encoded_text = tokenizer.encode(text=text, return_tensors="pt")
#
#     # Pass the encoded text to the DistilBERT model.
#     output = model(**encoded_text)
#
#     # Get the prediction from the DistilBERT model.
#     prediction = output[0].argmax(dim=-1)
#
#     # Classify the prediction as positive, negative, or neutral.
#     if prediction == 0:
#         return "Positive"
#     elif prediction == 1:
#         return "Negative"
#     else:
#         return "Neutral"
#
#
# if __name__ == "__main__":
#     # Get the text to be analyzed.
#     text = "I love this movie!"
#
#     # Perform sentiment analysis.
#     sentiment = sentiment_analysis(text)
#
#     # Print the sentiment.
#     print(sentiment)



# from tensorflow.keras.activations import relu # activation functions
# from tensorflow.keras.models import Sequential # NeuralNetwork models
# from tensorflow.keras.layers import Input, Dense, Dropout # NN layers
# from tensorflow.keras.losses import SparseCategoricalCrossentropy, CategoricalCrossentropy # error estimation
# from tensorflow.keras.optimizers import SGD, Adam # optimizers
#
# from tensorflow.keras.wrappers.scikit_learn import KerasRegressor