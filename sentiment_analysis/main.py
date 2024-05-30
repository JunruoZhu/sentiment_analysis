#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import os
import time
from argparse import ArgumentParser
from scipy import stats

from sentiment_analysis.visualize_result import visualize_results
from sentiment_analysis.process_folders import process_folder
from sentiment_analysis.significance import statistical_significance


def main():
    # Parse arguments
    parser = ArgumentParser(description="Perform sentiment scores, article number, and price for UST, LUNC, and FTX coin respectively.")
    args = parser.parse_args()

    folders = ["datasets/ust", 
    "datasets/ftx", 
    "datasets/lunc"
    ]
    result_base_folder = "results"

    if not os.path.exists(result_base_folder):
        os.makedirs(result_base_folder)

    pos_dfs = []
    neg_dfs = []
    price_dfs = []
    article_count_dfs = []

    # Compute sentiment scores of the articles for each coin
    for folder in folders:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Processing {folder}...")
        pos_df, neg_df, daily_articles_df, price_df = process_folder(folder)
        pos_dfs.append(pos_df)
        neg_dfs.append(neg_df)
        article_count_dfs.append(daily_articles_df)
        price_dfs.append(price_df)

        # Prepare the corresponding result folder
        subfolder_name = os.path.basename(folder)
        result_folder = os.path.join(result_base_folder, subfolder_name)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        # Visualize the results for each coin
        visualize_results(result_folder, pos_df, neg_df, price_df, daily_articles_df)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Visualization completed.")

        # Perform statistical tests for each coin
        results = statistical_significance(price_df, neg_df, pos_df, daily_articles_df)
        print(results)
       
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Statistical test completed.")

    print("=========== Complete! ===========")

if __name__ == "__main__":
    main()
