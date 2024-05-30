#!/usr/bin/python
# -*- coding: utf-8 -*-

"""to process price and article files in each subfolder. The process includes 
preprocessing, sentiment analysis, and results saving
"""

import os
import pandas as pd
from sentiment_analysis.preprocess import preprocess_main
from sentiment_analysis.calculate_sentiment import compute_sentiment
from sentiment_analysis.save_sentiment import save_sentiment

def process_folder(folder_name):
    # get the sub-folder's name
    subfolder_name = os.path.basename(folder_name)
    
    # create path
    input_path = os.path.join(folder_name, f'{subfolder_name}_articles.txt')
    output_path = os.path.join(folder_name, f'{subfolder_name}_scores.txt')
    price_file_path = os.path.join(folder_name, f'{subfolder_name}_price.txt')

    # Read files
    df = pd.read_csv(input_path)
    price_df = pd.read_csv(price_file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    price_df['Date'] = pd.to_datetime(price_df['Date'], format='%Y-%m-%d')

    # make sure 'id' is string
    df['id'] = df['id'].astype(str)

    # Preprocess articles
    df = preprocess_main(df)

    # Sentiment analysis
    results = compute_sentiment(df)

    # Save the sentiment scores
    pos_df, neg_df, daily_articles_df = save_sentiment(results, df, output_path)

    return pos_df, neg_df, daily_articles_df, price_df
