#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This script calculates text's sentiment values
"""
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import torch
import numpy as np
from scipy.special import softmax
import pandas as pd
from tqdm import tqdm


# Define a function computing the sentiment scores of a long text
def analyze_sentiment(text: str, tokenizer, model):
    # Tokenize the input with overflow handling
    encodings = tokenizer(text, return_tensors="pt",
                          return_overflowing_tokens=True,
                          stride=256,
                          truncation=True,
                          padding="longest",
                          max_length=512)

    # Handle each segment and collect scores
    all_scores = []
    for i in range(len(encodings["input_ids"])):
        segment = {k: v[i].unsqueeze(0) for k, v in encodings.items()}
        # Remove the argument not needed by the model
        segment.pop("overflow_to_sample_mapping", None)

        output = model(**segment)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        all_scores.append(scores)

    # Calculate the mean of the scores for all segments
    mean_scores = np.mean(all_scores, axis=0)
    sentiment_dict = {
        "neg": mean_scores[0],
        "neu": mean_scores[1],
        "pos": mean_scores[2]
    }

    return sentiment_dict


def compute_sentiment(corpus: pd.DataFrame) -> dict:
    """
    Produce the sentiment scores of each text
    """

    # print(torch.cuda.is_available())

    MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    # Ensure the model runs in CPU
    model = model.to("cpu")

    results = {}
    for i, row in tqdm(corpus.iterrows(), total=len(corpus)):
        try:
            text = str(row['Preprocessed_Content'])
            myid = row['id']

            result = analyze_sentiment(text, tokenizer, model)

            results[myid] = result
        except RuntimeError as e:
            print(f'Broke for id {myid}: {str(e)}')

    return results
